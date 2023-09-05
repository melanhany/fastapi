from sqlalchemy.orm import Session
from . import models, schemas

def get_stores_by_employee_phone(db: Session, phone_number: str):
    stores = db.query(models.Store) \
               .join(models.Employee) \
               .filter(models.Employee.phone_number == phone_number) \
               .all()
    return stores
