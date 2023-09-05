from pydantic import BaseModel
from datetime import datetime

# class OrderBase(BaseModel):
#     created_at: datetime
#     closed_at: datetime
    
# class Order(OrderBase):
#     id: int
#     store_id: int
#     author_id: int
#     executor_id: int

    
class EmployeeBase(BaseModel):
    name: str
    phone_number: str
    
class Employee(EmployeeBase):
    id: int
    store_id: int
    # orders: list[Order] = []
    

class StoreBase(BaseModel):
    name: str
    
class Store(StoreBase):
    id: int
    employees: list[Employee] = []

