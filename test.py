import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="HARSH8611@@&&##",
        database="sales_visit"
    )

    print("Connected successfully")

    conn.close()

except Exception as e:
    print(e)