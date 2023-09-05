from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from . import crud, models, schemas
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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/stores/")
def get_stores_for_employee(
    phone_number: str, 
    db: Session=Depends(get_db),
    response_model=list[schemas.Store] 
):
    stores = crud.get_stores_by_employee_phone(db=db, phone_number=phone_number)

    if not stores:
        raise HTTPException(status_code=404, detail="No stores found for the provided employee phone number")

    return stores