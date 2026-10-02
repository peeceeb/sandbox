from models.todo import Todo

class TodoManager:
    def __init__(self):
        self.todos={}
        self.next_id=1


    def create_todo(self, title, description):
        todo_id=self.next_id
        todo=Todo(todo_id,title,description)
        self.todos[todo_id]=todo
        self.next_id+=1
        return todo

    def update_todo(self, todo_id, title=None, description=None):
        if todo_id not in self.todos:
            print("Todo ID not found")
            return None

        todo = self.todos[todo_id]

        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description

        return todo
        

    def delete_todo(self, todo_id):
        if todo_id not in self.todos:
            print("Todo ID not found")
            return None

        todo=self.todos.pop(todo_id)
        return todo

    def print_all_todos(self):
        for todo_id, todo in self.todos.items():
            print(f"todo_id: {todo_id},\n"
                  f"title: {todo.title},\n"
                  f"description: {todo.description},\n"
                  f"completed: {todo.completed}")


    def mark_completed(self, todo_id, title=None, description=None):
            if todo_id not in self.todos:
                print("Todo ID not found")
                return None
    
            todo = self.todos[todo_id]
            
            todo.completed=True
    
            return todo