import sqlite3
import os
import re
 
# --- Global Variables ---
auto_show_after_add = True  # Boolean: Controls whether todos are displayed automatically after adding
DB_FILE = "todos.db"  # String: SQLite database file name
MAX_TODOS = 100  # Integer: Maximum allowed number of todos (for demonstration of a calculation)
 
# --- Database Initialization and Connection ---
def init_database():
    """Initializes the database and creates the 'todos' table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_FILE)  # Connect to the database
        cursor = conn.cursor()
        # Create the 'todos' table with ID (auto-increment) and task (text, not null)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        """)
        conn.commit()  # Save changes
        return conn, cursor
    except Exception as e:
        # Handle errors during database connection or table creation
        print(f"Error connecting to database or creating table: {e}")
        print(f"Please ensure '{DB_FILE}' can be created or accessed.")
        exit()
 
# --- Add Todo ---
def add_todo(cursor, conn, task):
    """Adds a new todo to the database and optionally displays all todos."""
    if task.strip():  # Check if task is not empty or just whitespace
        cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
        conn.commit()
        print("Todo added successfully.")
        if auto_show_after_add:
            show_todos(cursor)  # Show all todos if enabled
    else:
        print("Todo task cannot be empty. Please try again.")
 
# --- Show Todos ---
def show_todos(cursor):
    """Queries and displays all todos, including a count of todos."""
    cursor.execute("SELECT id, task FROM todos")
    rows = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM todos")  # SQL query to count the number of todos
    todo_count = cursor.fetchone()[0]
    if not rows:
        print("No todos found.")
    else:
        print(f"\nYour Todos (total: {todo_count}):")
        for row in rows:  # For loop to iterate through todos
            print(f"{row[0]}: {row[1]}")
        # Warn if maximum number of todos is reached
        if todo_count >= MAX_TODOS:
            print(f"Warning: Maximum number of {MAX_TODOS} todos reached.")
 
# --- Delete Todo ---
def delete_todo(cursor, conn, idx_input):
    """Deletes a todo based on the provided ID."""
    when = re.match(r"^[0-9]+$", idx_input)  # Check if input is a positive integer
    if when:
        idx = int(idx_input)
        cursor.execute("DELETE FROM todos WHERE id = ?", (idx,))
        if cursor.rowcount > 0:  # Check if a todo was deleted
            conn.commit()
            print("Todo deleted successfully.")
        else:
            print("Todo with this ID not found. Please enter a valid ID.")
    else:
        print("Invalid input. Please enter a valid number for the todo ID.")
 
# --- Main Program ---
def main():
    """Main program with menu loop and match case construct for user inputs."""
    conn, cursor = init_database()  # Initialize database

    while True:  # Main loop for the menu
        print("\n=== Todo App Menu ===")
        print("1. Add Todo")
        print("2. Show Todos")
        print("3. Delete Todo")
        print("4. Exit")

        choice = input("Choose an option: ")

        # Match case construct: Execute the corresponding action
        match choice:
            case "1":
                add_todo(cursor, conn, input("Enter your todo: "))
            case "2":
                show_todos(cursor)
            case "3":
                delete_todo(cursor, conn, input("Enter the number of the todo to delete: "))
            case "4":
                print("Exiting Todo App. Goodbye!")
                break  # Exit the loop
            case _:  # Default case for any other input
                print("Invalid option. Please choose 1, 2, 3, or 4.")

    # --- Close Database Connection ---
    conn.close()
# Start the program
if __name__ == "__main__":
    main()
