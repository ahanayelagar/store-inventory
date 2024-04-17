import pymysql
from creds import host, user, password, db

def mysqlconnect():
    # To connect MySQL database
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db
    )
    cur = conn.cursor()

    # Execute Query with joins
    cur.execute("""SELECT i.ID, i.description, i.price, c.name as category_name
                   FROM Inventory i
                   JOIN Category c ON i.categoryID = c.CategoryID
                   LIMIT 5""")
    output = cur.fetchall()
    
    # Print Results
    for row in output:
        print(row[0], "\t", row[1], "\t", row[2], "\t", row[3])
      
    # To close the connection
    conn.close()
  
# Driver Code
if __name__ == "__main__" :
    mysqlconnect()

