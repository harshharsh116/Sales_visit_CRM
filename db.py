import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="HARSH8611@@&&##",
        database="sales_visit"
    )


def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM users
    WHERE username = %s AND password = %s
    """

    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def save_visit(
    salesman,
    department,
    customer_name,
    area,
    visit_date,
    purpose,
    result,
    remarks,
    follow_up,
    followup_date,
    followup_objective
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO sales_visits (
        salesman,
        department,
        customer_name,
        area,
        visit_date,
        purpose,
        result,
        remarks,
        follow_up,
        followup_date,
        followup_objective
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            salesman,
            department,
            customer_name,
            area,
            visit_date,
            purpose,
            result,
            remarks,
            follow_up,
            followup_date,
            followup_objective
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_my_visits(salesman):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM sales_visits
    WHERE salesman = %s
    ORDER BY visit_date DESC
    """

    cursor.execute(query, (salesman,))
    visits = cursor.fetchall()

    cursor.close()
    conn.close()

    return visits
def get_all_visits():

    conn = get_connection()

    query = """
    SELECT *
    FROM sales_visits
    ORDER BY visit_date DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, full_name, username, role , email
        FROM users
        ORDER BY full_name
    """)

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

def add_user(full_name, username, password, role,email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (full_name, username, password, role,email)
        VALUES (%s,%s,%s,%s,%s)
    """, (full_name, username, password, role,email))

    conn.commit()

    cursor.close()
    conn.close()

def delete_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id=%s
    """, (user_id,))

    conn.commit()

    cursor.close()
    conn.close()

def total_visits():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sales_visits")

    total = cursor.fetchone()[0]

    conn.close()

    return total

def today_visits():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM sales_visits
        WHERE visit_date=CURDATE()
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def pending_followups():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM sales_visits
        WHERE follow_up='Yes'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def delete_visit(visit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM sales_visits WHERE visit_id=%s",
        (visit_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

def get_salesman_visits(salesman):
    conn = get_connection()

    query = """
        SELECT *
        FROM sales_visits
        WHERE salesman = %s
        ORDER BY visit_date DESC
    """

    df = pd.read_sql(query, conn, params=(salesman,))

    conn.close()

    return df
import pandas as pd

def get_salesman_visits_by_date(salesman, from_date, to_date):
    conn = get_connection()

    query = """
        SELECT *
        FROM sales_visits
        WHERE salesman = %s
        AND visit_date BETWEEN %s AND %s
        ORDER BY visit_date DESC
    """

    df = pd.read_sql(
        query,
        conn,
        params=(salesman, from_date, to_date)
    )

    conn.close()

    return df
