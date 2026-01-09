import random
import urllib.parse
from backend.database import SessionLocal
from backend import models

db = SessionLocal()

def update_images_reliable():
    items = db.query(models.Item).all()
    
    # Pastel colors palette (Hex codes)
    # Pink, Blue, Green, Yellow, Purple, Orange, Teal, Cyan
    pastel_colors = [
        "fbcfe8", # Pink
        "bbf7d0", # Green
        "fef08a", # Yellow
        "c7d2fe", # Purple/Blue
        "fed7aa", # Orange
        "a5f3fc", # Cyan
        "e9d5ff", # Purple
        "fecaca", # Red/Pink
        "ddd6fe", # Violet
        "99f6e4", # Teal
    ]
    
    count = 0
    for item in items:
        # Pick a random color seeded by ID to be deterministic
        random.seed(item.id)
        bg_color = random.choice(pastel_colors)
        text_color = "475569" # Slate-600, good contrast
        
        # URL encode the title to fit in the URL
        # Wrap text algorithm roughly or just truncate? 
        # placehold.co handles some text, but long text might look small.
        # Let's simple use the title.
        safe_title = urllib.parse.quote(item.title)
        
        # Dimensions: 300x450 (Standard Book/Poster Ratio 2:3)
        # Format: https://placehold.co/300x450/{bg}/{fg}?text={text}
        new_url = f"https://placehold.co/300x450/{bg_color}/{text_color}?text={safe_title}"
        
        item.cover_image_url = new_url
        count += 1
        
    db.commit()
    print(f"Updated {count} items with reliable pastel placeholders.")

if __name__ == "__main__":
    update_images_reliable()
