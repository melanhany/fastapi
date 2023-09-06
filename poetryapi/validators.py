from fastapi import Depends, HTTPException, status
from . import models, crud

from .database import SessionLocal, engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_employee_phone(phone_number: str):
    db = next(get_db())

    customer = crud.get_customer_by_phone(db, phone_number)
    
    if customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee phone number.")
    
    employee = crud.get_employee_by_phone(db, phone_number)

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    return phone_number
    
def validate_customer_phone(phone_number: str):
    db = next(get_db())
    
    employee = crud.get_employee_by_phone(db, phone_number)
    
    if employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid customer phone number.")

    customer = crud.get_customer_by_phone(db, phone_number)

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    return phone_number
    