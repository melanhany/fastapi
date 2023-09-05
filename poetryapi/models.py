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

    
    
    