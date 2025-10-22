# crud.py
# Isse database me items create/read/update/delete hote h

from sqlalchemy.orm import Session
import models, schemas

# Basic CRUD
def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# Extra/Custom APIs
def get_items_low_stock(db: Session, threshold: int = 5):
    return db.query(models.Item).filter(models.Item.quantity < threshold).all()

def get_items_by_product(db: Session, product_name: str):
    return db.query(models.Item).filter(models.Item.product == product_name).all()

def get_items_by_email(db: Session, email: str):
    return db.query(models.Item).filter(models.Item.email == email).all()

def get_items_by_name(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name.like(f"%{name}%")).all()
