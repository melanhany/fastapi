from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal, engine
from .validators import validate_employee_phone, validate_customer_phone

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
def get_stores_for_employee(
    phone_number: str = Depends(validate_employee_phone), 
    db: Session=Depends(get_db)
):
    stores = crud.get_stores_by_employee_phone(db=db, phone_number=phone_number)

    if not stores:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No stores found for the provided employee phone number")

    return stores

@app.get("/orders/", response_model=list[schemas.Order])
def get_orders_for_customer(
    phone_number: str = Depends(validate_customer_phone), 
    db: Session=Depends(get_db)
):
    orders = crud.get_orders_by_customer_phone(db, phone_number)
    
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No orders found for the provided customer phone number")
        
    return orders

@app.post("/orders/", response_model=schemas.Order)
def create_order_for_customer(
    order: schemas.OrderCreate, 
    phone_number: str = Depends(validate_customer_phone), 
    db: Session = Depends(get_db)
):
    customer = crud.get_customer_by_phone(db, phone_number)
    
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    author_id = customer.id    
    store_by_customer = crud.get_store_by_author(db, author_id)
    
    if order.store_id != store_by_customer.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can create order only for his store")
    
    store_by_executor = crud.get_store_by_executor(db, order.executor_id)
    
    if order.store_id != store_by_executor.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can create order with executor prescribed only for his store")
    
    return crud.create_customer_order(db, order, author_id)