from pydantic import BaseModel, Enum as PydanticEnum
from typing import Optional
from datetime import datetime

class OrderStatus(PydanticEnum):
    started = 'started'
    ended = 'ended'
    in_process = 'in process'
    awaiting = 'awaiting'
    canceled = 'canceled'

class OrderBase(BaseModel):
    store_id: int
    executor_id: int
    
class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class Order(OrderBase):
    id: int
    created_at: datetime
    closed_at: datetime
    author_id: int
    status: OrderStatus

    
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

