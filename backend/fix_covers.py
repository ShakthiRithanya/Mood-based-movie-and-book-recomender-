from backend.database import SessionLocal
from backend import models

db = SessionLocal()

def fix_specific_covers():
    # Specific manual fixes for broken items
    updates = {
        "The Great Gatsby": "https://upload.wikimedia.org/wikipedia/commons/7/7a/The_Great_Gatsby_Cover_1925_Retouched.jpg",
        "To Kill a Mockingbird": "https://upload.wikimedia.org/wikipedia/commons/4/4f/To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg"
    }

    for title, url in updates.items():
        item = db.query(models.Item).filter(models.Item.title == title).first()
        if item:
            item.cover_image_url = url
            print(f"Fixed cover for: {title}")
    
    db.commit()

if __name__ == "__main__":
    fix_specific_covers()
