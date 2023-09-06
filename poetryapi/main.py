from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
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

"""
Listing all stores for given employee
"""
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

"""
CRUD endpoints for orders 
"""
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

@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order_for_customer(
    order_id: int,
    phone_number: str = Depends(validate_customer_phone), 
    db: Session=Depends(get_db)
):
    order = crud.get_order_by_customer_phone(db, phone_number, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    return order


@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order_for_customer(
    order_id: int,
    updated_order: schemas.OrderUpdate,
    phone_number: str = Depends(validate_customer_phone), 
    db: Session=Depends(get_db)    
):
    order = crud.get_order_by_customer_phone(db, phone_number, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    customer = crud.get_customer_by_phone(db, phone_number)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    author_id = customer.id    
    store_by_customer = crud.get_store_by_author(db, author_id)
    store_by_executor = crud.get_store_by_executor(db, updated_order.executor_id)
    if updated_order.store_id:
        if updated_order.store_id != store_by_customer.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can update order only for his store")
        
        if store_by_executor is None or updated_order.store_id != store_by_executor.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can update order with executor prescribed only for his store")
    else:
        if store_by_executor is None or order.store_id != store_by_executor.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can update order with executor prescribed only for his store")
        
        
    for field, value in updated_order.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
        
    db.commit()
    db.refresh(order)

    return order

@app.delete("/orders/{order_id}", response_model=schemas.Order)
def delete_order(
    order_id: int, 
    phone_number: str = Depends(validate_customer_phone), 
    db: Session = Depends(get_db)
):
    order = crud.get_order_by_customer_phone(db, phone_number, order_id)
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    crud.delete_order(db, order_id)
    
    return order
    
@app.patch("/orders/{order_id}", response_model=schemas.Order)
def update_order_status(
    order_id: int,
    updated_order: schemas.OrderStatusUpdate,
    phone_number: str = Depends(validate_customer_phone), 
    db: Session=Depends(get_db)  
):
    order = crud.get_order_by_customer_phone(db, phone_number, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    customer = crud.get_customer_by_phone(db, phone_number)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    for field, value in updated_order.model_dump().items():
        setattr(order, field, value)
        
    db.commit()
    db.refresh(order)

    return order

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
    if store_by_executor is None or order.store_id != store_by_executor.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can create order with executor prescribed only for his store")
    
    return crud.create_customer_order(db, order, author_id)

"""
CRUD endpoints for visits
"""
@app.get("/visits/", response_model=list[schemas.Visit])
def get_visits_for_customer(
    phone_number: str = Depends(validate_customer_phone),
    db: Session=Depends(get_db)
):
    visits = crud.get_visits_by_customer_phone(db, phone_number)
    
    if not visits:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No visits found for the provided customer phone number")
        
    return visits

@app.get("/visits/{visit_id}", response_model=schemas.Visit)
def get_visit_for_customer(
    visit_id: int,
    phone_number: str = Depends(validate_customer_phone), 
    db: Session=Depends(get_db)
):
    visit = crud.get_visit_by_customer_phone(db, phone_number, visit_id)
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    return visit

@app.post("/visits/", response_model=schemas.Visit)
def create_visit_for_customer(
    visit: schemas.VisitCreate, 
    phone_number: str = Depends(validate_customer_phone), 
    db: Session = Depends(get_db)
):
    customer = crud.get_customer_by_phone(db, phone_number)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    author_id = customer.id
    store_by_customer = crud.get_store_by_author(db, author_id)
    if visit.store_id != store_by_customer.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can create visit only for his store")
    
    customer_order = crud.get_customer_order(db, author_id, visit.order_id)
    if customer_order is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can create visit only for his order")
    
    order = crud.get_order_by_customer_phone(db, phone_number, visit.order_id)
    if order.visit:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can create visit for his order that doesn't already have visit")     
    
    if order.executor == visit.executor_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer can create visit with executor prescribed only for his order")
    
    return crud.create_customer_visit(db, visit, author_id)
