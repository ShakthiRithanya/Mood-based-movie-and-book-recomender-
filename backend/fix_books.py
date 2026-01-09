from backend.database import SessionLocal
from backend import models

db = SessionLocal()

def fix_book_urls():
    items = db.query(models.Item).filter(models.Item.type == "book").all()
    
    count = 0
    for item in items:
        # Check if it's an OpenLibrary URL
        if "covers.openlibrary.org" in item.cover_image_url:
            # Check if it already has params?
            if "?default=false" not in item.cover_image_url:
                item.cover_image_url = item.cover_image_url + "?default=false"
                count += 1
                
    db.commit()
    print(f"Updated {count} book URLs to force 404 on failure.")

if __name__ == "__main__":
    fix_book_urls()
