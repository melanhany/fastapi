from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import Union, Optional
from enum import Enum as PythonEnum
from datetime import datetime

class OrderStatus(str, PythonEnum):
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
    store_id: Optional[int] = None
    executor_id: Optional[int] = None

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class Order(OrderBase):
    id: int
    created_at: datetime
    closed_at: Union[datetime, None] = None 
    author_id: int
    status: OrderStatus

class VisitBase(BaseModel):
    store_id: int
    executor_id: int
    order_id: int
    
class VisitCreate(VisitBase):
    pass

class VisitUpdate(VisitBase):
    store_id: Optional[int] = None
    executor_id: Optional[int] = None
    order_id: Optional[int] = None

class Visit(VisitBase):
    id: int
    created_at: datetime
    author_id: int
    
class EmployeeBase(BaseModel):
    name: str
    phone_number: str
    
class Employee(EmployeeBase):
    id: int


class StoreBase(BaseModel):
    name: str
    
class Store(StoreBase):
    id: int
    employees: list[Employee] = []

