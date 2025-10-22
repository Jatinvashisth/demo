# main.py
# Isse API run hote h

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal, Base, engine
import models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory + Contacts Management System")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Basic CRUD (5 APIs) ---
@app.post("/items/", response_model=schemas.Item)
def create_item_api(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@app.get("/items/", response_model=list[schemas.Item])
def read_items_api(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_items(db, skip, limit)

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item_api(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item: raise HTTPException(404, "Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item_api(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id, item)
    if not db_item: raise HTTPException(404, "Item not found")
    return db_item

@app.delete("/items/{item_id}")
def delete_item_api(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id)
    if not db_item: raise HTTPException(404, "Item not found")
    return {"message": "Item deleted successfully"}

# --- Custom APIs (5 APIs) ---
@app.get("/items/low-stock/", response_model=list[schemas.Item])
def low_stock_items(threshold: int = 5, db: Session = Depends(get_db)):
    return crud.get_items_low_stock(db, threshold)

@app.get("/items/by-product/{product_name}", response_model=list[schemas.Item])
def items_by_product(product_name: str, db: Session = Depends(get_db)):
    return crud.get_items_by_product(db, product_name)

@app.get("/items/by-email/{email}", response_model=list[schemas.Item])
def items_by_email(email: str, db: Session = Depends(get_db)):
    return crud.get_items_by_email(db, email)

@app.get("/items/by-name/{name}", response_model=list[schemas.Item])
def items_by_name(name: str, db: Session = Depends(get_db)):
    return crud.get_items_by_name(db, name)

@app.get("/items/search/", response_model=list[schemas.Item])
def search_items(name: str = "", product: str = "", db: Session = Depends(get_db)):
    query = db.query(models.Item)
    if name: query = query.filter(models.Item.name.like(f"%{name}%"))
    if product: query = query.filter(models.Item.product.like(f"%{product}%"))
    return query.all()
