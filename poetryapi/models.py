from enum import Enum as PythonEnum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum, event
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    employees = relationship("Employee", back_populates="store")
    customers = relationship("Customer", back_populates="store")
    orders = relationship("Order", back_populates="store")
    visits = relationship("Visit", back_populates="store")
    

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    phone_number = Column(String(255))
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    
    store = relationship("Store", back_populates="customers")
    orders = relationship("Order", back_populates="author")
    visits = relationship("Visit", back_populates="author")
    
    
class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    phone_number = Column(String(255))
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    
    store = relationship("Store", back_populates="employees")
    orders = relationship("Order", back_populates="executor")
    visits = relationship("Visit", back_populates="executor")

    
class OrderStatus(str, PythonEnum):
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
    visit = relationship("Visit", back_populates="order", uselist=False)
    
@event.listens_for(Order.status, 'set')
def _update_closed_at(target, value, oldvalue, initiator):
    if value in (OrderStatus.ended, OrderStatus.canceled) and target.closed_at is None:
        target.closed_at = func.now()


class Visit(Base):
    __tablename__ = "visits"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
    executor_id = Column(Integer, ForeignKey("employees.id"))
    author_id = Column(Integer, ForeignKey("customers.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))
    
    order = relationship("Order", back_populates="visit")
    executor = relationship("Employee", back_populates="visits")
    author = relationship("Customer", back_populates="visits")
    store = relationship("Store", back_populates="visits")
    