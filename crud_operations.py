import mysql.connector

config = {
    'host': 'localhost',
    'port': 3308,  # Change this to your MySQL port if different
    'user': 'root',
    'password': '',
    'database': 'pycrud'
}

def connect_to_database():
    try:
        conn = mysql.connector.connect(**config)
        print("Connected to MySQL database!")
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def close_connection(conn, cursor=None):
    try:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("MySQL connection closed.")
    except mysql.connector.Error as e:
        print(f"Error closing connection: {e}")

def insert_data(conn, data_to_insert):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO studentrecord (name, reg, mobile) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data_to_insert['name'], data_to_insert['reg'], data_to_insert['mobile']))
        conn.commit()
        print("Data inserted successfully!")
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")

def update_data(conn, data_to_update):
    try:
        cursor = conn.cursor()
        sql = "UPDATE studentrecord SET mobile = %s WHERE id = %s"
        cursor.execute(sql, (data_to_update['mobile'], data_to_update['id']))
        conn.commit()
        print("Data updated successfully!")
    except mysql.connector.Error as e:
        print(f"Error updating data: {e}")

def delete_data(conn, record_id_to_delete):
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM studentrecord WHERE id = %s"
        cursor.execute(sql, (record_id_to_delete,))
        conn.commit()
        print("Data deleted successfully!")
    except mysql.connector.Error as e:
        print(f"Error deleting data: {e}")

def read_data(conn):
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM studentrecord"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows is None:
            print("No data found.")
            return []
        else:
            for row in rows:
                print(row)
            return rows
    except mysql.connector.Error as e:
        print(f"Error reading data: {e}")
        return []  # Return an empty list to indicate failure