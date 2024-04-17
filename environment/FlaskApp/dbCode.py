import pymysql
from creds import host, user, password, db
from flask import Flask, render_template

app = Flask(__name__)

def get_conn():
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
    )
    return conn

def execute_query(query, args=()):
    cur = get_conn().cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

# Display the query results in an HTML table
def display_html(rows):
    html = """<table>
                <tr>
                    <th>Inventory ID</th>
                    <th>Description</th>
                    <th>Price</th>
                    <th>Category ID</th>
                </tr>"""

    for r in rows:
        html += "<tr>"
        for value in r:
            html += "<td>" + str(value) + "</td>"
        html += "</tr>"
    
    html += "</table>"
    return html

# Define your Flask route
@app.route("/viewdb")
def viewdb():
    # Modify the SQL query to fetch data from your ProjectOneStore database
    rows = execute_query("""SELECT ID, description, price, categoryID FROM inventory LIMIT 500""")
    return display_html(rows)
