class Todo:
    def __init__(self,todo_id,title,description,completed=False) -> None:
        self.todo_id=todo_id
        self.title=title
        self.description=description
        self.completed=completed
