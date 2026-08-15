from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class Address(BaseModel):
    street:str
    city:str
    zip_code:str

class User(BaseModel):
    id:int
    name: str
    email: str
    is_active: bool
    createdAt: datetime
    address: Address
    tags: List[str]=[]
    model_config=ConfigDict(json_encoders={datetime: lambda v: v.strftime('%d-%m-%Y %H:%M:%S')})

user = User(id=1, 
            name="Prasanna",
            email="bagal.prasanna@gmail.com", 
            createdAt=datetime(2026,5,31,17,26),
            address=Address(
                    street="High Street",
                    city="Baner",
                    zip_code="411045"),
            is_active=False,
            tags=["premium","subscriber"]
    )

python_dict=user.model_dump()
print(python_dict)
print(user)
print("="*30)
    
json_str = user.model_dump_json
print("="*30)
print(json_str)

