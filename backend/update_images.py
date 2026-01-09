from backend.database import SessionLocal
from backend import models

db = SessionLocal()

def update_images():
    items = db.query(models.Item).all()
    
    # Extensive mapping of title -> Real/Thematic Cover URL
    real_covers = {
        # Movies
        "The Godfather": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "The Shawshank Redemption": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_FMjpg_UX1000_.jpg",
        "Schindler's List": "https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg",
        "Raging Bull": "https://m.media-amazon.com/images/M/MV5BYjRmODkzNDItMTNhNi00YjJlLTg0M2QtODkzYSBhZTBkZThkXkEyXkFqcGdeQXVyNzQ1ODk3MTQ@._V1_FMjpg_UX1000_.jpg",
        "Casablanca": "https://m.media-amazon.com/images/M/MV5BY2IzZGY2YmEtYzljNS00NTM5LTgwMzUtMzM1NjQ4NGI0OTk0XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_FMjpg_UX1000_.jpg",
        "Citizen Kane": "https://m.media-amazon.com/images/M/MV5BYjBiOTYxZWItMzdiZi00NjlkLWIzZTYtYmFhZjhiMTljOTIyXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "Gone with the Wind": "https://m.media-amazon.com/images/M/MV5BYjUyZWZkM2UtMzYxYy00ZmU3LWE0NzQtYWJjMzJhZWM4ZTZhXkEyXkFqcGdeQXVyMNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "The Wizard of Oz": "https://m.media-amazon.com/images/M/MV5BNjUyMTc4MDExMV5BMl5BanBnXkFtZTgwNDg0NDIwMjE@._V1_FMjpg_UX1000_.jpg",
        "One Flew Over the Cuckoo's Nest": "https://m.media-amazon.com/images/M/MV5BZjA0OWVhOTAtYWQxNi00YzNhLWI4ZGItYzhkZWU1MTc2ZGVmXkEyXkFqcGdeQXVyMTZjFjFmOA@@._V1_FMjpg_UX1000_.jpg",
        "Lawrence of Arabia": "https://m.media-amazon.com/images/M/MV5BYWY5ZjhjNGYtZmI2Ny00ODM0LWFkNzgtZmI1YzA2NADBkYjQxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "Vertigo": "https://m.media-amazon.com/images/M/MV5BYTE4ODEwZDUtNDFjOC00NjAxLWEzYTQtYTI1NGVmZmFlNjdiL2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_FMjpg_UX1000_.jpg",
        "Psycho": "https://m.media-amazon.com/images/M/MV5BNTQwNDM1YzItNDAxZC00NWY2LTk0M2UtNDIwNWI5OGUyNWUxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "The Silence of the Lambs": "https://m.media-amazon.com/images/M/MV5BNjNhZTk0ZmEtNjJhMi00YzFlLWE1MmEtYzM1M2ZmMGMwMTU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg",
        "Chinatown": "https://m.media-amazon.com/images/M/MV5BMjJkMDZhYzItZTFhdy00ZWZhLThhMGItMWFlMTAxZDBkNmRjXkEyXkFqcGdeQXVyMDI2NDg0NQ@@._V1_FMjpg_UX1000_.jpg",
        "Star Wars: Episode IV - A New Hope": "https://m.media-amazon.com/images/M/MV5BOTA5NjhiOTAtZWM0ZC00MWNhLThiMzEtZDFkOTk2OTU1ZDJkXkEyXkFqcGdeQXVyMTA4NDI1NTQx._V1_FMjpg_UX1000_.jpg",
        "The Lord of the Rings: The Fellowship of the Ring": "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_FMjpg_UX1000_.jpg",
        "Amélie": "https://m.media-amazon.com/images/M/MV5BNDg4NjM1YjMtYmNhZC00MjM0LWFiZmYtNGY1YjYzNjgwOTIyXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "Eternal Sunshine of the Spotless Mind": "https://m.media-amazon.com/images/M/MV5BMTY4NzcwODg3Nl5BMl5BanBnXkFtZTcwNTEwOTMyMw@@._V1_FMjpg_UX1000_.jpg",
        "The Pianist": "https://m.media-amazon.com/images/M/MV5BOWRiZDIxZjktMTA1NC00MDQ2LWEzMjUtMTliZmY3NjQ3ODJiXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg",
        "Gladiator": "https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg",
        "Titanic": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_FMjpg_UX1000_.jpg",
        "The Lion King": "https://m.media-amazon.com/images/M/MV5BYTYxNGMyZTYtMjE3MS00MzNjLWFjNmYtMDk3N2FmM2JiM2M1XkEyXkFqcGdeQXVyNjY5NDU4NzI@._V1_FMjpg_UX1000_.jpg",
        "Back to the Future": "https://m.media-amazon.com/images/M/MV5BZmU0M2Y1OGUtZjIxNi00ZjBkLTg1MjgtOWIyNThiZWIwYjRiXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg",
        "Alien": "https://m.media-amazon.com/images/M/MV5BOGQzZTBjMjQtOTVmMS00NGE5LWEyYmEtOGQyZTc3ZWI5YjJkXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_FMjpg_UX1000_.jpg",
        "The Shining": "https://m.media-amazon.com/images/M/MV5BZWFlYmY2MGEtZjVkYS00YzU4LTg0YjQtYzY1ZGE3NTA5NGQxXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg",
        "Whiplash": "https://m.media-amazon.com/images/M/MV5BOTA5NDZlZGUtMjAxOS00YTRkLTkwYmMtYWQ0NWEwZDZiNjEzXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX1000_.jpg",
        "La La Land": "https://m.media-amazon.com/images/M/MV5BMzUzNDM2NzM2MV5BMl5BanBnXkFtZTgwNTM3NTg4OTE@._V1_FMjpg_UX1000_.jpg",
        "Joker": "https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_FMjpg_UX1000_.jpg",
        "Avengers: Infinity War": "https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_FMjpg_UX1000_.jpg",
        "Inception": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_FMjpg_UX1000_.jpg",
        "Fight Club": "https://m.media-amazon.com/images/M/MV5BMmEzNTkxYjQtZTc0MC00YTVjLTg5ZTEtZWMwOWVlYzY0NWIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "Pulp Fiction": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "Forrest Gump": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg",
        "The Matrix": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg",
        "Interstellar": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX1000_.jpg",
        "Parasite": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_FMjpg_UX1000_.jpg",
        "The Dark Knight": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwOTA0N15BMl5BanBnXkFtZTcwMDYzIxNw@@._V1_FMjpg_UX1000_.jpg",
        "Star Wars: Episode V - The Empire Strikes Back": "https://m.media-amazon.com/images/M/MV5BYmU1NDRjNDgtMzhiMi00NjZmLTg5NGItZDNiZjU5NTU4OTE0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "Goodfellas": "https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI4ZmQtMjIwYjFjNmI3ZGEwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "Se7en": "https://m.media-amazon.com/images/M/MV5BOTUwODM5MTctZjczMi00OTk4LTg3NWUtNmVhMTAzNTNjYjcyXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg",
        "Seven Samurai": "https://m.media-amazon.com/images/M/MV5BOWE4YWVjZjUtYTE1ZC00YzJiLWI3MzQtMzk5ZmVlNWJkN2NmXkEyXkFqcGdeQXVyMTUzMDUzNTI3._V1_FMjpg_UX1000_.jpg",
        "It's a Wonderful Life": "https://m.media-amazon.com/images/M/MV5BZjc4NDZhZWMtNGEzYS00ZWU2LThlM2ItNTA0YzQ0OTExMTE2XkEyXkFqcGdeQXVyNjUwNzk3NDc@._V1_FMjpg_UX1000_.jpg",
        "City of God": "https://m.media-amazon.com/images/M/MV5BOTMwYjc5ZmItYTFjZC00ZGQ3LThiZTktOTZhN2ZkZmEjZEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg",
        "Saving Private Ryan": "https://m.media-amazon.com/images/M/MV5BZjhkMDM4MWItZTVjOC00ZDRhLThmYTAtM2I5NzBmNmNlMzI1XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_FMjpg_UX1000_.jpg",
        "The Green Mile": "https://m.media-amazon.com/images/M/MV5BMTUxMzQyNjA5MF5BMl5BanBnXkFtZTYwOTU2NTY3._V1_FMjpg_UX1000_.jpg",
        "Spirited Away": "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZZhT=GhaMTUzMWY0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "Life Is Beautiful": "https://m.media-amazon.com/images/M/MV5BYmJmM2Q4NmMtYThmNC00ZjRlLWEyZmItZTIwOTBlZDQ3NTQ1XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg",

        # Books
        "Don Quixote": "https://i.pinimg.com/564x/0f/6f/a0/0f6fa076e73c4f7461bf035ba5966456.jpg",
        "A Tale of Two Cities": "https://i.pinimg.com/564x/6a/d0/0d/6ad00db95e67a5df7a0d42129ba09ce7.jpg",
        "The Little Prince": "https://i.pinimg.com/564x/0f/10/7b/0f107b22a0e28659103e659b81404c09.jpg",
        "Harry Potter and the Chamber of Secrets": "https://i.pinimg.com/564x/6c/1a/02/6c1a0296765799a77685652516668352.jpg",
        "The Catcher in the Rye": "https://i.pinimg.com/564x/44/d5/07/44d50711cc080ca9e102f4a56a6428eb.jpg",
        "The Hobbit": "https://i.pinimg.com/564x/a4/0c/36/a40c36357bd707692224098939c0179a.jpg",
        "Fahrenheit 451": "https://i.pinimg.com/564x/92/83/88/92838883648025218764036612176435.jpg",
        "The Odyssey": "https://i.pinimg.com/564x/eb/64/46/eb644654948834ecabf1345d44445341.jpg",
        "War and Peace": "https://i.pinimg.com/564x/af/02/43/af0243187c3a074092497645068469ad.jpg",
        "Hamlet": "https://i.pinimg.com/564x/c6/8e/31/c68e317c49615a97531776ce350a4023.jpg",
        "Moby Dick": "https://i.pinimg.com/564x/0a/60/a6/0a60a6a0242250280227189914aba82d.jpg",
        "The Divine Comedy": "https://i.pinimg.com/564x/94/d5/ae/94d5ae25227786423ce976150372df3e.jpg",
        "The Brothers Karamazov": "https://i.pinimg.com/564x/78/39/2e/78392e2764b8849156f7129532588383.jpg",
        "Anna Karenina": "https://i.pinimg.com/564x/54/10/cd/5410cd99e5672d56683cff5696191b22.jpg",
        "Brave New World": "https://i.pinimg.com/564x/72/7a/12/727a1262d580796216440263309a9634.jpg",
        "Wuthering Heights": "https://i.pinimg.com/564x/d5/cd/6d/d5cd6d8c063cf9c7717614272186786c.jpg",
        "Frankenstein": "https://i.pinimg.com/564x/77/b6/20/77b6208803451670984950346bf66380.jpg",
        "Alice's Adventures in Wonderland": "https://i.pinimg.com/564x/94/39/39/94393952723329f6fc18413669675271.jpg",
        "The Picture of Dorian Gray": "https://i.pinimg.com/564x/02/98/95/029895c276329068069502758172901e.jpg",
        "Catch-22": "https://i.pinimg.com/564x/e7/03/6e/e7036ee268c171092499d21466039572.jpg",
        "The Stranger": "https://i.pinimg.com/564x/f1/b7/66/f1b76686a6058e3902998782a17058ab.jpg",
        "Heart of Darkness": "https://i.pinimg.com/564x/fc/55/75/fc5575c2e37e58319084824699569651.jpg",
        "Gulliver's Travels": "https://i.pinimg.com/564x/87/b9/e6/87b9e671ad869389100803527f050221.jpg",
        "Les Misérables": "https://i.pinimg.com/564x/e4/fb/20/e4fb209e7019c4902b2ef42023023249.jpg",
        "The Grapes of Wrath": "https://i.pinimg.com/564x/e4/42/4f/e4424f11400e960256424564c489710f.jpg",
        "Of Mice and Men": "https://i.pinimg.com/564x/f0/dd/4f/f0dd4fe498e2741d48858102a0614144.jpg",
        "A Game of Thrones": "https://i.pinimg.com/564x/87/34/00/873400539c394c868478498877543881.jpg",
        "It": "https://i.pinimg.com/564x/31/53/38/315338006d649232326757053075249f.jpg",
        "1984": "https://i.pinimg.com/564x/b8/0e/e6/b80ee61f924dfd014022026858e9949b.jpg",
        "To Kill a Mockingbird": "https://i.pinimg.com/564x/28/76/85/287685e82415174092b700994648702c.jpg",
        "The Great Gatsby": "https://i.pinimg.com/564x/e0/7d/53/e07d532585c57223e75e117462551ddc.jpg",
        "Pride and Prejudice": "https://i.pinimg.com/564x/72/77/89/727789f2425482381272da6813fa9435.jpg",
        "The Diary of a Young Girl": "https://i.pinimg.com/564x/d1/02/75/d102758bfd3067484469f649bfdb655f.jpg",
        "The Book Thief": "https://i.pinimg.com/564x/e2/56/67/e25667c4fa4e892cfa7175968b571171.jpg",
        "Little Women": "https://i.pinimg.com/564x/9b/7f/05/9b7f0564614397334751717354966606.jpg",
        "Jane Eyre": "https://i.pinimg.com/564x/c7/2b/86/c72b864a66860d84428753232b700e57.jpg",
        "Animal Farm": "https://i.pinimg.com/564x/11/a3/bb/11a3bb9356da3dfd9c02db391264c7ad.jpg",
        "The Kite Runner": "https://i.pinimg.com/564x/36/35/66/3635667ab8eb875e523f46f3801f4c3a.jpg",
        "The Hunger Games": "https://i.pinimg.com/564x/6c/20/d2/6c20d2d326d9715d9da684a0c8491c10.jpg",
        "Harry Potter and the Sorcerer's Stone": "https://i.pinimg.com/564x/d3/18/34/d31834241e3d309071c77864f77c385b.jpg",
        "Slaughterhouse-Five": "https://i.pinimg.com/564x/7b/d5/36/7bd53641617253393963428989508544.jpg",
        "The Lord of the Rings": "https://i.pinimg.com/564x/ff/3d/26/ff3d2673235b27230b809886326e5a6a.jpg",
        "The Chronicles of Narnia": "https://i.pinimg.com/564x/73/19/d7/7319d7d42ae583f6190892c90c379796.jpg",
        "The Alchemist": "https://i.pinimg.com/564x/16/09/cc/1609cc694b4198cc7645064e628469b6.jpg",
        "The Da Vinci Code": "https://i.pinimg.com/564x/93/bf/ec/93bfeca1f5f244199c09199676e107ce.jpg",
        "Crime and Punishment": "https://i.pinimg.com/564x/5a/2a/3a/5a2a3a1f81216d16cc2016467384236a.jpg",
        "Dune": "https://i.pinimg.com/564x/24/ce/20/24ce204128fec41589146ec6877144e5.jpg",
    }
    
    unique_count = 0
    for item in items:
        # Check if we have a real cover
        if item.title in real_covers:
            item.cover_image_url = real_covers[item.title]
        else:
            # Fallback for uniqueness: Random Image from picsum seed
            # We use seed={item.id} to ensure it stays the same/consistent for that ID
            # but is different from every other item.
            # Using 300x450 vertical ratio
            if item.type == 'movie':
                 item.cover_image_url = f"https://picsum.photos/seed/{item.id + 1000}/300/450"
            else:
                 item.cover_image_url = f"https://picsum.photos/seed/{item.id}/300/450"
        unique_count += 1
        
    db.commit()
    print(f"Updated {unique_count} items with unique images.")

if __name__ == "__main__":
    update_images()
