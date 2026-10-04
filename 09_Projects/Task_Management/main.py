from services.task_service import Task_Service
from services.user_service import User_Service

def main():

    task_service=Task_Service()
    user_service=User_Service()

    user_service.add_User(123, "Prasanna", "bagal.prasanna@gmail.com")
    task_service.create_task(1,"Deloitte Interview", "Revise concepts of Modeling ")
    task_service.create_task(2, "Complete Office Work", "Run Result validation task")
    task_service.create_task(3, "Gym", "Workout Shoulders and Abs")

    task_service.complete_task()
    task_service.complete_task()
    task_service.complete_task()

    history=task_service.get_task_history()
    while not history.is_empty(): 
        print(history.pop().title) 
    


if __name__ == "__main__":
    main()