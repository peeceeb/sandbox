from models.Todo import Todo

class TodoManager():
    def __init__(self):
        self.storage={}
        self.next_id=1

    def create_todo(self,title,description):
        todo_id=self.next_id
        obj=Todo(todo_id,title,description,completed=False)
        self.storage[todo_id]=obj
        self.next_id+=1
        return obj
        
    def update_todo(self):
        pass

    def delete_todo(self):
        pass

    def print_all_todos(self):
         for todo_id, todo in self.storage.items():
            print(f"todo_id: {todo_id},\n"
                  f"title: {todo.title},\n"
                  f"description: {todo.description},\n"
                  f"completed: {todo.completed}")
