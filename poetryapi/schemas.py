from pydantic import BaseModel, Enum as PydanticEnum
from typing import Optional
from datetime import datetime

# class OrderStatus(PydanticEnum):
#     started = 'started'
#     ended = 'ended'
#     in_process = 'in process'
#     awaiting = 'awaiting'
#     canceled = 'canceled'

# class OrderBase(BaseModel):
#     status: OrderStatus
    
# class OrderCreate(OrderBase):
#     store_id: Optional[int]
#     author_id: Optional[int]
#     executor_id: Optional[int]
#     status    

# class Order(OrderBase):
#     id: int

    
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

