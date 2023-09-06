from sqlalchemy.orm import Session
from . import models, schemas

def get_stores_by_employee_phone(db: Session, phone_number: str):
    return db.query(models.Store) \
                .join(models.Employee) \
                .filter(models.Employee.phone_number == phone_number) \
                .all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer) \
                .filter(models.Customer.id == customer_id) \
                .first()

def get_customer_by_phone(db: Session, phone_number: str):
    return db.query(models.Customer) \
                .filter(models.Customer.phone_number == phone_number).first()
