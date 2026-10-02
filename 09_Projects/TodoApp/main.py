from services.todo_manager import TodoManager


def main():
    manager = TodoManager()

    while True:
        print("\n===== TODO APP =====")
        print("1. Create Todo")
        print("2. Update Todo")
        print("3. Delete Todo")
        print("4. Complete Todo")
        print("5. Show All Todos")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter title: ")
            description = input("Enter description: ")

            task = manager.create_todo(title, description)

            print(f"Todo created successfully. ID: {task.todo_id}")

        elif choice == "2":
            todo_id = int(input("Enter Todo ID: "))

            title = input("Enter new title (press Enter to keep existing): ")
            description = input(
                "Enter new description (press Enter to keep existing): "
            )

            title = title if title else None
            description = description if description else None

            task = manager.update_todo(
                todo_id,
                title,
                description
            )

            if task:
                print("Todo updated successfully.")

        elif choice == "3":
            todo_id = int(input("Enter Todo ID to delete: "))

            task = manager.delete_todo(todo_id)

            if task:
                print(f"Todo '{task.title}' deleted successfully.")

        elif choice == "4":
            todo_id = int(input("Enter Todo ID to complete: "))

            task = manager.complete_todo(todo_id)

            if task:
                print(f"Todo '{task.title}' marked as completed.")

        elif choice == "5":
            manager.print_all_todos()

        elif choice == "6":
            print("Exiting Todo App...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()