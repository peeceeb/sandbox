from services.TodoManager import TodoManager

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

        choice= input("Enter your choice\n")

        if choice in ('1'):
            title = input("Enter the title\n")
            description = input("Enter the description\n")
            task=manager.create_todo(title,description)
            print("Todo Created Successfully",{task.id})

        elif choice == ('5'):
            manager.print_all_todos()

        elif choice in ('6'):
            print("\n Exiting to do app")
            break

        else:
            print("\n Invalid choice selected")
            break


        





if __name__ == "__main__":
    main()