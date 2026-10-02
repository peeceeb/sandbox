class TaskNotFoundException(Exception):
    def __init__(self, message="Task Not Found"):
        super().__init__(message)

    

class TodoItem:
    def __init__(self, todo_id, title, is_completed=False):
        self.todo_id=todo_id
        self.title=title
        self.is_completed=is_completed    



Milk=TodoItem(1,"Milk",True)
Dahi=TodoItem(2,"Dahi",True)
Salt=TodoItem(3,"Salt",True)



