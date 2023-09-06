from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal, engine

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get("/stores/", response_model=list[schemas.Store])
def get_stores_for_employee(phone_number: str, db: Session=Depends(get_db)):
    stores = crud.get_stores_by_employee_phone(db=db, phone_number=phone_number)

    if not stores:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No stores found for the provided employee phone number")

    return stores

@app.get("/orders/", response_model=list[schemas.Order])
def get_orders_for_customer(phone_number: str, db: Session=Depends(get_db)):
    orders = crud.get_orders_by_customer_phone(db, phone_number)
    
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No orders found for the provided customer phone number")
        
    return orders