from typing import List, Optional
from pydantic import BaseModel


class Address(BaseModel):  #User Defined datatype
    street: str
    city: str
    postal_code: str

class User(BaseModel):
    id: int
    name: str
    address: Address #Pydantic validates address as well


address_prasanna=Address(street="401 Pearl",city="Pune", postal_code="411045")
user_prasanna=User(id=1,name="Prasanna",address=address_prasanna)
print(user_prasanna)

user_data={"id":1, "name":"Tushar","address":{"street":"Main Street", "city":"Pimple Saudagar","postal_code":"400101"}}

user_Tushar=User(**user_data)
print(user_Tushar)
