from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool

input_data= {'id':101, 'name': "Chaicode", 'is_active': True}


user = User(**input_data) #unpack the dictionary using ** Always unpack the dictionary

print(user)