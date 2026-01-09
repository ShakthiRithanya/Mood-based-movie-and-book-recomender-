from backend.database import SessionLocal, engine
from backend import models

db = SessionLocal()

def count_items():
    book_count = db.query(models.Item).filter(models.Item.type == "book").count()
    movie_count = db.query(models.Item).filter(models.Item.type == "movie").count()
    
    print(f"Books: {book_count}")
    print(f"Movies: {movie_count}")
    print(f"Total: {book_count + movie_count}")

if __name__ == "__main__":
    count_items()
