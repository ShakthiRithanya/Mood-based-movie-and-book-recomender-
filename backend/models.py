from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="student") # student, admin
    
    ratings = relationship("Rating", back_populates="user")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    type = Column(String) # book, movie
    author_or_director = Column(String)
    genres = Column(String)
    year = Column(Integer)
    language = Column(String)
    description = Column(Text)
    cover_image_url = Column(String, nullable=True)
    availability_status = Column(String, default="Available")
    
    ratings = relationship("Rating", back_populates="item")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    rating = Column(Integer) # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ratings")
    item = relationship("Item", back_populates="ratings")
