import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        sql = "INSERT INTO studentrecord (name, roll, course) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data_to_insert['name'], data_to_insert['roll'], data_to_insert['course']))
        conn.commit()
        messagebox.showinfo("Information", "Data inserted successfully!")
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")
        messagebox.showerror("Error", f"Failed to insert data: {e}")

def update_data(conn, data_to_update):
    try:
        cursor = conn.cursor()
        sql = "UPDATE studentrecord SET course = %s WHERE roll = %s"
        cursor.execute(sql, (data_to_update['course'], data_to_update['roll']))
        conn.commit()
        messagebox.showinfo("Information", "Data updated successfully!")
    except mysql.connector.Error as e:
        print(f"Error updating data: {e}")
        messagebox.showerror("Error", f"Failed to update data: {e}")

def delete_data(conn, roll_to_delete):
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM studentrecord WHERE roll = %s"
        cursor.execute(sql, (roll_to_delete,))
        conn.commit()
        messagebox.showinfo("Information", "Data deleted successfully!")
    except mysql.connector.Error as e:
        print(f"Error deleting data: {e}")
        messagebox.showerror("Error", f"Failed to delete data: {e}")

def read_data(conn):
    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM studentrecord"
        cursor.execute(sql)
        rows = cursor.fetchall()
        messagebox.showinfo("Information", "Data read successfully!")
        return rows
    except mysql.connector.Error as e:
        print(f"Error reading data: {e}")
        messagebox.showerror("Error", f"Failed to read data: {e}")
        return []

def on_insert_button_click():
    data_to_insert = {
        'name': name_entry.get(),
        'roll': roll_entry.get(),
        'course': course_entry.get()
    }
    insert_data(conn, data_to_insert)

def on_update_button_click():
    data_to_update = {
        'roll': roll_entry.get(),
        'course': course_entry.get()
    }
    update_data(conn, data_to_update)

def on_delete_button_click():
    roll_to_delete = roll_entry.get()
    delete_data(conn, roll_to_delete)

def on_read_button_click():
    rows = read_data(conn)
    if rows:
        show_data(rows)

def show_data(rows):
    data_window = tk.Toplevel(root)
    data_window.title("Data from Database")

    tree = ttk.Treeview(data_window)
    tree["columns"] = ("Name", "Roll", "Course")
    tree.heading("#0", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Roll", text="Roll")
    tree.heading("Course", text="Course")

    for row in rows:
        tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3]))

    tree.pack(expand=True, fill="both")

def create_gui():
    root = tk.Tk()
    root.title("MySQL Database GUI")

    # Create labels and entry fields for data input
    tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Roll:").grid(row=1, column=0, padx=10, pady=5)
    roll_entry = tk.Entry(root)
    roll_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Course:").grid(row=2, column=0, padx=10, pady=5)
    course_entry = tk.Entry(root)
    course_entry.grid(row=2, column=1, padx=10, pady=5)

    # Create Insert, Update, Delete, Read buttons
    insert_button = tk.Button(root, text="Insert", command=on_insert_button_click)
    insert_button.grid(row=3, column=0, padx=5, pady=5)

    update_button = tk.Button(root, text="Update", command=on_update_button_click)
    update_button.grid(row=3, column=1, padx=5, pady=5)

    delete_button = tk.Button(root, text="Delete", command=on_delete_button_click)
    delete_button.grid(row=3, column=2, padx=5, pady=5)

    read_button = tk.Button(root, text="Read", command=on_read_button_click)
    read_button.grid(row=3, column=3, padx=5, pady=5)

    return root, name_entry, roll_entry, course_entry

conn = connect_to_database()
if conn:
    root, name_entry, roll_entry, course_entry = create_gui()
    root.mainloop()
else:
    print("Cannot connect to the database.")