from models.Graph import Graph
from models.Queue import Queue
from models.Stack import Stack
from models.Task import Task
from models.User import User

class Task_Service:
    def __init__(self): 
        self.tasks=[]
        self.task_queue=Queue()
        self.task_history = Stack()


    def create_task(self, id, title, description):
        task = Task(id, title, description)
        self.tasks.append(task)
        self.task_queue.enqueue(task)
        return task
    

    def complete_task(self):
        if not self.task_queue.is_empty():
            task = self.task_queue.dequeue()
            self.task_history.push(task)
            return task.title
        return None

    def get_task_history(self) -> Stack:
        return self.task_history    

    

