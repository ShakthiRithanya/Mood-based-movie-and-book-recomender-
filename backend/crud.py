from sqlalchemy.orm import Session
from . import models, schemas, auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    # First user is admin for simplicity or special email
    role = "student"
    if "admin" in user.email:
         role = "admin"
         
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100, search: str = None, type: str = None):
    query = db.query(models.Item)
    if search:
        query = query.filter(models.Item.title.contains(search) | models.Item.author_or_director.contains(search))
    if type:
        query = query.filter(models.Item.type == type)
    return query.offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_rating(db: Session, rating: schemas.RatingCreate, user_id: int):
    # Check if exists
    existing = db.query(models.Rating).filter(models.Rating.user_id == user_id, models.Rating.item_id == rating.item_id).first()
    if existing:
        existing.rating = rating.rating
        db.commit()
        db.refresh(existing)
        return existing
    
    db_rating = models.Rating(**rating.dict(), user_id=user_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating
