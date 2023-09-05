from enum import Enum as PythonEnum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    phone_number = Column(String(255))
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    
    store = relationship("Store", back_populates="employees")
    
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    phone_number = Column(String(255))
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    
    store = relationship("Store", back_populates="customers")

    
class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    employees = relationship("Employee", back_populates="store")

    
class OrderStatus(PythonEnum):
    started = 'started'
    ended = 'ended'
    in_process = 'in process'
    awaiting = 'awaiting'
    canceled = 'canceled'

    
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True))
    store_id = Column(Integer, ForeignKey("stores.id"))
    author_id = Column(Integer, ForeignKey("customers.id"))
    executor_id = Column(Integer, ForeignKey("employees.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.awaiting)
    
    store = relationship("Store", back_populates="orders")
    author = relationship("Customer", back_populates="orders")
    executor = relationship("Employee", back_populates="orders")
    
    # Set up an event listener to update closed_at when is_closed becomes True
    @staticmethod
    def _update_closed_at(mapper, connection, target):
        if target.status in (OrderStatus.ended, OrderStatus.canceled) and target.closed_at is None:
            target.closed_at = func.now()
