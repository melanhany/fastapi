from sqlalchemy.orm import Session
from . import models, schemas

def get_employee_by_phone(db: Session, phone_number: str):
    return db.query(models.Employee) \
                .filter(models.Employee.phone_number == phone_number) \
                .first()

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
                .filter(models.Customer.phone_number == phone_number) \
                .first()

def get_orders_by_customer_phone(db: Session, phone_number: str):
    return db.query(models.Order) \
                .join(models.Customer) \
                .filter(models.Customer.phone_number == phone_number) \
                .all()
                
def create_customer_order(db: Session, order: schemas.OrderCreate, customer_phone: str):
    customer = db.query(models.Customer) \
                    .filter(models.Customer.phone_number == customer_phone) \
                    .first()
    db_order = models.Order(**order.model_dump(), author_id=customer.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order