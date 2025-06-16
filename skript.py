import sqlite3
import os
import re

# Database file name
DB_FILE = "todos.db"

# --- Database Initialization and Connection ---
try:
    # Connect to the SQLite database. If the file doesn't exist, it will be created.
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the 'todos' table if it doesn't already exist.
    # 'id' is an auto-incrementing primary key.
    # 'task' stores the todo description and cannot be empty.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)
    conn.commit()  # Save the table creation
except Exception as e:
    # Handle connection or table creation errors
    print(f"Error connecting to database or creating table: {e}")
    print(f"Please ensure '{DB_FILE}' can be created or accessed, and that you have necessary permissions.")
    exit() # Corrected from 'Exit' to 'exit()'

# --- Main Application Loop ---
while True:
    print("\n=== Todo App Menu ===")
    print("1. Add Todo")
    print("2. Show Todos")
    print("3. Delete Todo")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        # Add a new todo task
        task = input("Enter your todo: ")
        if task.strip(): # Ensure task is not empty or just whitespace
            cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
            conn.commit()
            print("Todo added successfully.")
        else:
            print("Todo task cannot be empty. Please try again.")

    elif choice == "2":
        # Show all existing todo tasks
        cursor.execute("SELECT id, task FROM todos")
        rows = cursor.fetchall()
        if not rows:
            print("No todos found.")
        else:
            print("Your Todos:")
            for row in rows:
                print(f"{row[0]}: {row[1]}")

    elif choice == "3":
        # Delete a todo task by its ID
        idx_input = input("Enter the number of the todo to delete: ")
        # Validate input to ensure it's a positive integer
        if re.match(r"^[0-9]+$", idx_input):
            idx = int(idx_input)
            cursor.execute("DELETE FROM todos WHERE id = ?", (idx,))
            if cursor.rowcount > 0:
                # If a row was actually deleted, commit the change
                conn.commit()
                print("Todo deleted successfully.")
            else:
                # If no row was deleted, the ID was not found
                print("Todo with that ID not found. Please try again with a valid ID.")
        else:
            print("Invalid input. Please enter a valid number for the todo ID.")

    elif choice == "4":
        # Exit the application
        print("Exiting Todo App. Goodbye!")
        break

    else:
        # Handle invalid menu choices
        print("Invalid option. Please choose from 1, 2, 3, or 4.")

# --- Close the database connection when the loop exits ---
conn.close()

