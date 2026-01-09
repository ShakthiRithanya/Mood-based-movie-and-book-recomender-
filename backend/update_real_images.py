import urllib.parse
from backend.database import SessionLocal
from backend import models

db = SessionLocal()

def update_real_images():
    items = db.query(models.Item).all()
    
    # Wikimedia/Official Poster URLs (Manual Mapping for High Quality)
    movie_posters = {
        "The Godfather": "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_ver1.jpg",
        "The Shawshank Redemption": "https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg",
        "Schindler's List": "https://upload.wikimedia.org/wikipedia/en/3/38/Schindler%27s_List_movie.jpg",
        "Raging Bull": "https://upload.wikimedia.org/wikipedia/en/5/5f/Raging_Bull_poster.jpg",
        "Casablanca": "https://upload.wikimedia.org/wikipedia/commons/b/b3/CasablancaPoster-Gold.jpg",
        "Citizen Kane": "https://upload.wikimedia.org/wikipedia/en/c/ce/Citizenkane.jpg",
        "Gone with the Wind": "https://upload.wikimedia.org/wikipedia/commons/2/27/Poster_-_Gone_With_the_Wind_01.jpg",
        "The Wizard of Oz": "https://upload.wikimedia.org/wikipedia/commons/6/6e/The_Wizard_of_Oz_1939_poster.png",
        "One Flew Over the Cuckoo's Nest": "https://upload.wikimedia.org/wikipedia/en/2/26/One_Flew_Over_the_Cuckoo%27s_Nest_poster.jpg",
        "Lawrence of Arabia": "https://upload.wikimedia.org/wikipedia/en/c/c5/Lawrence_of_arabia_ver3_xxlg.jpg",
        "Vertigo": "https://upload.wikimedia.org/wikipedia/en/7/75/Vertigomovie_restoration.jpg",
        "Psycho": "https://upload.wikimedia.org/wikipedia/en/b/b9/Psycho_%281960%29_theatrical_poster_%2B.jpg",
        "The Silence of the Lambs": "https://upload.wikimedia.org/wikipedia/en/8/86/The_Silence_of_the_Lambs_poster.jpg",
        "Chinatown": "https://upload.wikimedia.org/wikipedia/en/2/2d/Chinatown_%281974_movie_poster%29.jpg",
        "Star Wars: Episode IV - A New Hope": "https://upload.wikimedia.org/wikipedia/en/8/87/StarWarsMoviePoster1977.jpg",
        "The Lord of the Rings: The Fellowship of the Ring": "https://upload.wikimedia.org/wikipedia/en/8/8a/The_Lord_of_the_Rings_The_Fellowship_of_the_Ring_%282001%29.jpg",
        "Amélie": "https://upload.wikimedia.org/wikipedia/en/5/53/Amelie_poster.jpg",
        "Eternal Sunshine of the Spotless Mind": "https://upload.wikimedia.org/wikipedia/en/a/a4/Eternal_Sunshine_of_the_Spotless_Mind_Poster.jpg",
        "The Pianist": "https://upload.wikimedia.org/wikipedia/en/a/a6/The_Pianist_poster.jpg",
        "Gladiator": "https://upload.wikimedia.org/wikipedia/en/f/fb/Gladiator_%282000_film_poster%29.png",
        "Titanic": "https://upload.wikimedia.org/wikipedia/en/1/18/Titanic_%281997_film%29_poster.png",
        "The Lion King": "https://upload.wikimedia.org/wikipedia/en/3/3d/The_Lion_King_poster.jpg",
        "Back to the Future": "https://upload.wikimedia.org/wikipedia/en/d/d2/Back_to_the_Future.jpg",
        "Alien": "https://upload.wikimedia.org/wikipedia/en/c/c3/Alien_movie_poster.jpg",
        "The Shining": "https://upload.wikimedia.org/wikipedia/en/1/18/The_Shining_1980.jpg",
        "Whiplash": "https://upload.wikimedia.org/wikipedia/en/0/01/Whiplash_poster.jpg",
        "La La Land": "https://upload.wikimedia.org/wikipedia/en/a/ab/La_La_Land_%28film%29.png",
        "Joker": "https://upload.wikimedia.org/wikipedia/en/e/e1/Joker_%282019_film%29_poster.jpg",
        "Avengers: Infinity War": "https://upload.wikimedia.org/wikipedia/en/4/4d/Avengers_Infinity_War_poster.jpg",
        "Inception": "https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg",
        "Fight Club": "https://upload.wikimedia.org/wikipedia/en/f/fc/Fight_Club_poster.jpg",
        "Pulp Fiction": "https://upload.wikimedia.org/wikipedia/en/3/3b/Pulp_Fiction_%281994%29_poster.jpg",
        "Forrest Gump": "https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg",
        "The Matrix": "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg",
        "Interstellar": "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",
        "Parasite": "https://upload.wikimedia.org/wikipedia/en/5/53/Parasite_%282019_film%29.png",
        "The Dark Knight": "https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg",
        "Star Wars: Episode V - The Empire Strikes Back": "https://upload.wikimedia.org/wikipedia/en/3/3c/SW_-_Empire_Strikes_Back.jpg",
        "Goodfellas": "https://upload.wikimedia.org/wikipedia/en/7/7b/Goodfellas.jpg",
        "Se7en": "https://upload.wikimedia.org/wikipedia/en/6/68/Seven_%281995_film%29_poster.jpg",
        "Seven Samurai": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Seven_Samurai_poster.jpg",
        "It's a Wonderful Life": "https://upload.wikimedia.org/wikipedia/en/1/10/It%27s_a_Wonderful_Life_%281946_poster%29.jpeg",
        "City of God": "https://upload.wikimedia.org/wikipedia/en/1/10/City_of_God_%282002_film%29_poster.jpg",
        "Saving Private Ryan": "https://upload.wikimedia.org/wikipedia/en/a/ac/Saving_Private_Ryan_poster.jpg",
        "The Green Mile": "https://upload.wikimedia.org/wikipedia/en/e/e2/The_Green_Mile_%28movie_poster%29.jpg",
        "Spirited Away": "https://upload.wikimedia.org/wikipedia/en/d/db/Spirited_Away_Japanese_poster.png",
        "Life Is Beautiful": "https://upload.wikimedia.org/wikipedia/en/7/7c/Vitaebella.jpg",
    }
    
    count = 0
    for item in items:
        # Use OpenLibrary for books (reliable public API)
        if item.type == 'book':
            # Encode title for URL (safe format)
            encoded_title = urllib.parse.quote(item.title.replace(" ", "_"))
            item.cover_image_url = f"https://covers.openlibrary.org/b/title/{encoded_title}-L.jpg"
            count += 1
            
        elif item.type == 'movie':
            if item.title in movie_posters:
                item.cover_image_url = movie_posters[item.title]
            else:
                # Fallback to a placeholder that looks better than nothing, 
                # or rely on similar title match? 
                # Let's keep the pastel fallback for unknown movies so it's not broken
                # But we have covered almost all the ones we seeded.
                # If unforeseen, use a generic movie reel image from Unsplash
                 if "placehold.co" in item.cover_image_url:
                     item.cover_image_url = "https://images.unsplash.com/photo-1542204165-65bf26472b9b?auto=format&fit=crop&q=80&w=300&h=450"
            count += 1
            
    db.commit()
    print(f"Updated {count} items with real posters/covers.")

if __name__ == "__main__":
    update_real_images()
