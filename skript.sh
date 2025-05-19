#!/bin/bash

# Initialize the todos array by reading from the file
todos=()
if [ -f todos.txt ]; then
    while IFS= read -r line; do
        todos+=("$line")
    done < todos.txt
else
    echo "Creating new todos.txt file."
    touch todos.txt
fi

# Main loop
while true; do
    echo -e "\n=== Todo App Menu ==="
    echo "1. Add Todo"
    echo "2. Show Todos"
    echo "3. Delete Todo"
    echo "4. Exit"
    read -p "Choose an option: " choice

    case $choice in
        1)
            read -p "Enter your todo: " task
            todos+=("$task")
            ;;
        2)
            if [ ${#todos[@]} -eq 0 ]; then
                echo "No todos found."
            else
                echo "Your Todos:"
                for i in "${!todos[@]}"; do
                    echo "$((i+1)): ${todos[$i]}"
                done
            fi
            ;;
        3)
            read -p "Enter the number of the todo to delete: " idx
            if [[ "$idx" =~ ^[0-9]+$ ]] && [ "$idx" -ge 1 ] && [ "$idx" -le ${#todos[@]} ]; then
                unset todos[$((idx-1))]
                todos=("${todos[@]}") # Re-index array
                echo "Todo deleted."
            else
                echo "Invalid index. Please try again."
            fi
            ;;
        4)
            echo "Exiting Todo App."
            break
            ;;
        *)
            echo "Invalid option. Please choose from 1 to 4."
            ;;
    esac

    # Write todos to file after each action
    > todos.txt
    for todo in "${todos[@]}"; do
        echo "$todo" >> todos.txt
    done
done
