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
                
def get_store_by_author(db: Session, author_id: int):
    return db.query(models.Store) \
                .join(models.Customer) \
                .filter(models.Customer.id == author_id) \
                .first()

def get_store_by_executor(db: Session, executor_id: int):
    return db.query(models.Store) \
                .join(models.Employee) \
                .filter(models.Employee.id == executor_id) \
                .first()

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
def get_order_by_customer_phone(db: Session, phone_number: str, order_id: int):
    return db.query(models.Order) \
                .join(models.Customer) \
                .filter(models.Customer.phone_number == phone_number) \
                .filter(models.Order.id == order_id) \
                .first()

def get_store(db: Session, store_id: int):
    return db.query(models.Store) \
                .filter(models.Store.id == store_id) \
                .first()
                
def create_customer_order(db: Session, order: schemas.OrderCreate, customer_id: int):
    db_order = models.Order(**order.model_dump(), author_id=customer_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if order:
        db.delete(order)
        db.commit()


