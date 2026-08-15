from typing import Optional
from pydantic import BaseModel, Field
import re

class Employee(BaseModel):
    id: int
    name: str=Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee Name",
        examples="Prasanna Bagal"
    )

    department: Optional[str] = "Risk"

    salary: float = Field(
        ...,
        ge=10000,
        le=1000000,
        description="Annual Salary in USD"
    )

class User(BaseModel):
    email: str = Field(...,regex=r'')
    phone: str = Field(...,regex=r'')
    age: int = Field(...,ge=0,le=150,description="Age in years")
    discount: float=Field(..., ge=0,le=100, description="Discount percentage")


    