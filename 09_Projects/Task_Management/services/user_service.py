from models.User import User

class User_Service():
    def __init__(self) -> None:
        self.users={}

    def add_User(self, id, name, email):
        user=User(name,id,email)
        self.users[id]=user
        return user

    def get_user(self, id):
        return self.users.get(id)

    