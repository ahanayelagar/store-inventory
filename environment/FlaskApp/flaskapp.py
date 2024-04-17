from flask import Flask, render_template, request, redirect, url_for
from dbCode import execute_query, get_conn
import boto3


app = Flask(__name__)
table_name = "Users"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""
        SELECT i.ID, i.description, i.price, c.name as category_name
        FROM Inventory i
        LEFT JOIN Category c ON i.categoryID = c.CategoryID
        ORDER BY i.ID
    """)
    return render_template('Viewdb.html', rows=rows)

@app.route("/homepage")
def homepage():
    return render_template('homepage.html')
    
# Route to render form for adding a new item
@app.route("/add", methods=["GET"])
def add_item_form():
    return render_template("add_item.html")

# Route to handle adding a new item
@app.route("/add", methods=["POST"])
def add_item():
    description = request.form.get("description")
    price = request.form.get("price")
    category_id = request.form.get("category_id")
    error_message = None

    conn = get_conn()
    cur = conn.cursor()

    try:
        # Check if an item with the same description already exists
        cur.execute("SELECT COUNT(*) FROM Inventory WHERE description = %s", (description,))
        count = cur.fetchone()[0]

        if count == 0:
            # If no item with the same description exists, insert the new item
            cur.execute("INSERT INTO Inventory (description, price, categoryID) VALUES (%s, %s, %s)", (description, price, category_id))
            conn.commit()
        else:
            # If an item with the same description already exists, set an error message
            error_message = "Sorry! We couldn't add the item to the list because it already exists! :("
    except Exception as e:
        # If an error occurs, rollback the transaction and set an appropriate error message
        conn.rollback()
        error_message = f"Error: {str(e)}"
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

    # Fetch all items from the inventory
    rows = execute_query("SELECT * FROM Inventory")

    # Render the template with the error message and inventory items
    return render_template("Viewdb.html", rows=rows, error_message=error_message)
    

# Route to display the delete item form
@app.route("/delete", methods=["GET"])
def delete_item_form():
    return render_template("delete_item.html")


# Route to handle deleting an item
@app.route("/delete", methods=["POST"])
def delete_item():
    description = request.form.get("description")

    conn = get_conn()
    cur = conn.cursor()

    try:
        # Attempt to delete the item from the inventory
        cur.execute("DELETE FROM Inventory WHERE description = %s", (description,))
        if cur.rowcount == 0:
            # If no rows were affected, it means the item does not exist
            error_message = "Item does not exist in the inventory"
            return render_template("delete_item.html", error_message=error_message)
        else:
            conn.commit()
            success_message = "Item deleted successfully"
            return render_template("delete_item.html", success_message=success_message)
    except Exception as e:
        # If an error occurs, rollback the transaction and set an appropriate error message
        conn.rollback()
        error_message = f"Error: {str(e)}"
        return render_template("delete_item.html", error_message=error_message)
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
    
# Route to render form for updating an item
@app.route("/update", methods=["GET"])
def update_item_form():
    return render_template("update_item.html", error_message="", success_message="")

# Route to handle updating an item
@app.route("/update", methods=["POST"])
def update_item():
    old_description = request.form.get("old_description")
    new_description = request.form.get("new_description")
    price = request.form.get("price")
    category_id = request.form.get("category_id")

    conn = get_conn()
    cur = conn.cursor()

    # Initialize success_message and error_message variables
    success_message = ""
    error_message = ""

    try:
        # Check if the provided category_id exists in the Category table
        cur.execute("SELECT COUNT(*) FROM Category WHERE CategoryID = %s", (category_id,))
        category_exists = cur.fetchone()[0]

        if category_exists:
            # Attempt to update the item in the inventory
            cur.execute("UPDATE Inventory SET description = %s, price = %s, categoryID = %s WHERE description = %s", (new_description, price, category_id, old_description))
            if cur.rowcount == 0:
                # If no rows were affected, it means the item does not exist
                error_message = "Item does not exist in the inventory"
            else:
                conn.commit()
                success_message = "Item updated successfully"
        else:
            # If the category does not exist, set an error message
            error_message = "Category does not exist"
    except Exception as e:
        # If an error occurs, rollback the transaction and set an appropriate error message
        conn.rollback()
        error_message = f"Error: {str(e)}"
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

    # Render the update_item.html template with the appropriate messages
    return render_template("update_item.html", error_message=error_message, success_message=success_message)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            # Attempt to retrieve user data from DynamoDB
            response = table.get_item(Key={"username": username})
            if "Item" in response:
                # Username exists, check if password matches
                if response["Item"]["password"] == password:
                    # Password is correct, redirect to the homepage
                    return redirect(url_for("homepage"))
                else:
                    error_message = "Username already taken / Incorrect password"
                    return render_template("login.html", error_message=error_message)
            else:
                # Username not found, insert new user into DynamoDB
                table.put_item(Item={"username": username, "password": password})
                success_message = "Account created successfully"
                return render_template("login.html", success_message=success_message)
        except Exception as e:
            # Handle any exceptions that occur during DynamoDB operation
            error_message = f"Error: {str(e)}"
            return render_template("login.html", error_message=error_message)
    else:
        return render_template("login.html")

def create_user():
    # This function is called from the main method to create a user
    # It inserts a sample username and password into the DynamoDB table
    sample_username = "sample_user"
    sample_password = "sample_password"
    table.put_item(Item={"username": sample_username, "password": sample_password})

        
        
if __name__ == "__main__":
    create_user()
    app.run(host='0.0.0.0', port=8080, debug=True)
