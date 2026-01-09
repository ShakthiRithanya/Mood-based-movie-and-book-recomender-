import random
from .database import SessionLocal, engine
from . import models
from .auth import get_password_hash

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

def get_cover(title, type_):
    # Mapping specific popular titles to real(ish) covers or high quality aesthetic shots
    covers = {
        "The Godfather": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
        "Pulp Fiction": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
        "Fight Club": "https://m.media-amazon.com/images/M/MV5BMmEzNTkxYjQtZTc0MC00YTVjLTg5ZTEtZWMwOWVlYzY0NWIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
        "Inception": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg",
        "Forrest Gump": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg",
        "The Matrix": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg",
        "The Lord of the Rings: The Fellowship of the Ring": "https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_.jpg",
        "Spirited Away": "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZZhT=GhaMTUzMWY0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
        "Interstellar": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
        "Parasite": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_.jpg",
        "The Dark Knight": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwOTA0N15BMl5BanBnXkFtZTcwMDYzIxNw@@._V1_.jpg",
        "1984": "https://images.unsplash.com/photo-1535905557558-afc4877a26fc?auto=format&fit=crop&q=80&w=300&h=450", # Dystopian vibe
        "To Kill a Mockingbird": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=300&h=450",
        "Harry Potter and the Sorcerer's Stone": "https://images.unsplash.com/photo-1618666012174-83b441c0bc76?auto=format&fit=crop&q=80&w=300&h=450", # Magical vibe
        "The Great Gatsby": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?auto=format&fit=crop&q=80&w=300&h=450",
        "Dune": "https://images.unsplash.com/photo-1541963463532-d68292c34b19?auto=format&fit=crop&q=80&w=300&h=450",
    }
    
    if title in covers:
        return covers[title]
    
    # Random aesthetics for others
    book_images = [
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&q=80&w=300&h=450",
        "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&q=80&w=300&h=450",
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=300&h=450",
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&q=80&w=300&h=450",
    ]
    movie_images = [
        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&q=80&w=300&h=450", # Cinema reel
        "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?auto=format&fit=crop&q=80&w=300&h=450", # Projector
        "https://images.unsplash.com/photo-1478720568477-152d9b164e63?auto=format&fit=crop&q=80&w=300&h=450", # Film
        "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=300&h=450", # Dark cinema
    ]
    
    if type_ == "book":
        return random.choice(book_images)
    return random.choice(movie_images)

def seed():
    # Only adding new items if they don't exist
    existing_titles = {item.title for item in db.query(models.Item).all()}
    
    # 1. Ensure Users exist
    if not db.query(models.User).filter(models.User.email == "admin@college.edu").first():
        admin = models.User(email="admin@college.edu", hashed_password=get_password_hash("admin123"), role="admin")
        db.add(admin)
    
    # 2. Huge List
    items_source = [
        # Movies
        ("The Godfather", "movie", "Francis Ford Coppola", "Crime, Drama", 1972, "English", "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."),
        ("The Shawshank Redemption", "movie", "Frank Darabont", "Drama", 1994, "English", "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."),
        ("Schindler's List", "movie", "Steven Spielberg", "Biography, Drama, History", 1993, "English", "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce."),
        ("Raging Bull", "movie", "Martin Scorsese", "Biography, Drama, Sport", 1980, "English", "The life of boxer Jake LaMotta, whose violence and temper that led him to the top in the ring destroyed his life outside of it."),
        ("Casablanca", "movie", "Michael Curtiz", "Drama, Romance, War", 1942, "English", "A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover and her fugitive husband escape the Nazis in French Morocco."),
        ("Citizen Kane", "movie", "Orson Welles", "Drama, Mystery", 1941, "English", "Following the death of publishing tycoon Charles Foster Kane, reporters scramble to uncover the meaning of his final utterance; 'Rosebud'."),
        ("Gone with the Wind", "movie", "Victor Fleming", "Drama, History, Romance", 1939, "English", "The manipulative daughter of a Georgia plantation owner conducts a turbulent romance with a roguish profiteer during the American Civil War."),
        ("The Wizard of Oz", "movie", "Victor Fleming", "Adventure, Family, Fantasy", 1939, "English", "Dorothy Gale is swept away from a farm in Kansas to a magical land of Oz in a tornado and embarks on a quest with her new friends to see the Wizard who can help her return home."),
        ("One Flew Over the Cuckoo's Nest", "movie", "Milos Forman", "Drama", 1975, "English", "A criminal pleads insanity and is admitted to a mental institution, where he rebels against the oppressive nurse and rallies up the scared patients."),
        ("Lawrence of Arabia", "movie", "David Lean", "Adventure, Biography, Drama", 1962, "English", "The story of T.E. Lawrence, the English officer who successfully united and led the diverse, often warring, Arab tribes during World War I in order to fight the Turks."),
        ("Vertigo", "movie", "Alfred Hitchcock", "Mystery, Romance, Thriller", 1958, "English", "A former police detective juggles wrestling with his personal demons and becoming obsessed with a hauntingly beautiful woman."),
        ("Psycho", "movie", "Alfred Hitchcock", "Horror, Mystery, Thriller", 1960, "English", "A Phoenix secretary embezzles $40,000 from her employer's client, goes on the run, and checks into a remote motel run by a young man under the domination of his mother."),
        ("The Silence of the Lambs", "movie", "Jonathan Demme", "Crime, Drama, Thriller", 1991, "English", "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims."),
        ("Chinatown", "movie", "Roman Polanski", "Drama, Mystery, Thriller", 1974, "English", "A private detective hired to expose an adulterer finds himself caught up in a web of deceit, corruption, and murder."),
        ("Star Wars: Episode IV - A New Hope", "movie", "George Lucas", "Action, Adventure, Fantasy", 1977, "English", "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station."),
        ("The Lord of the Rings: The Fellowship of the Ring", "movie", "Peter Jackson", "Action, Adventure, Drama", 2001, "English", "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron."),
        ("Amélie", "movie", "Jean-Pierre Jeunet", "Comedy, Romance", 2001, "French", "Amélie is an innocent and naive girl in Paris with her own sense of justice. She decides to help those around her and, along the way, discovers love."),
        ("Eternal Sunshine of the Spotless Mind", "movie", "Michel Gondry", "Drama, Romance, Sci-Fi", 2004, "English", "When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories."),
        ("The Pianist", "movie", "Roman Polanski", "Biography, Drama, Music", 2002, "English", "A Polish Jewish radio station pianist struggles for survival in the Warsaw Ghetto of World War II."),
        ("Gladiator", "movie", "Ridley Scott", "Action, Adventure, Drama", 2000, "English", "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery."),
        ("Titanic", "movie", "James Cameron", "Drama, Romance", 1997, "English", "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."),
        ("The Lion King", "movie", "Roger Allers", "Animation, Adventure, Drama", 1994, "English", "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself."),
        ("Back to the Future", "movie", "Robert Zemeckis", "Adventure, Comedy, Sci-Fi", 1985, "English", "Marty McFly, a 17-year-old high school student, is accidentally sent thirty years into the past in a time-traveling DeLorean invented by his close friend, the eccentric scientist Doc Brown."),
        ("Alien", "movie", "Ridley Scott", "Horror, Sci-Fi", 1979, "English", "After a space merchant vessel receives an unknown transmission as a distress call, one of the crew is attacked by a mysterious life form and they soon realize that its life cycle has merely begun."),
        ("The Shining", "movie", "Stanley Kubrick", "Drama, Horror", 1980, "English", "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings from the past and of the future."),
        ("Whiplash", "movie", "Damien Chazelle", "Drama, Music", 2014, "English", "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential."),
        ("La La Land", "movie", "Damien Chazelle", "Comedy, Drama, Music", 2016, "English", "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future."),
        ("Joker", "movie", "Todd Phillips", "Crime, Drama, Thriller", 2019, "English", "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime. This path brings him face-to-face with his alter-ego: the Joker."),
        ("Avengers: Infinity War", "movie", "Anthony Russo", "Action, Adventure, Sci-Fi", 2018, "English", "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe."),
        # Books
        ("Don Quixote", "book", "Miguel de Cervantes", "Classic, Adventure", 1605, "Spanish", "The adventures of a noble (hidalgo) from La Mancha named Alonso Quxano, who reads so many chivalric romances that he loses his mind and decides to become a knight-errant."),
        ("A Tale of Two Cities", "book", "Charles Dickens", "Historical, Fiction", 1859, "English", "London and Paris before and during the French Revolution: the story of the French Doctor Manette, his 18-year-long imprisonment in the Bastille in Paris and his release to live in London with his daughter Lucie."),
        ("The Little Prince", "book", "Antoine de Saint-Exupéry", "Fantasy, Fiction", 1943, "French", "A classic novella about a young prince who visits various planets in space, including Earth, and addresses themes of loneliness, friendship, love, and loss."),
        ("Harry Potter and the Chamber of Secrets", "book", "J.K. Rowling", "Fantasy, Fiction", 1998, "English", "Harry Potter's second year at Hogwarts School of Witchcraft and Wizardry, during which a series of messages on the walls of the school's corridors warn that the 'Chamber of Secrets' has been opened."),
        ("The Catcher in the Rye", "book", "J.D. Salinger", "Fiction, Classic", 1951, "English", "Holden Caulfield, a teenage protagonist, narrates his own story of teenage angst and alienation."),
        ("The Hobbit", "book", "J.R.R. Tolkien", "Fantasy, Fiction", 1937, "English", "Bilbo Baggins, a hobbit, is convinced by the wizard Gandalf to accompany thirteen dwarves, led by Thorin Oakenshield, on a quest to reclaim the Lonely Mountain from the dragon Smaug."),
        ("Fahrenheit 451", "book", "Ray Bradbury", "Dystopian, Sci-Fi", 1953, "English", "A future American society where books are outlawed and 'firemen' burn any that are found."),
        ("The Odyssey", "book", "Homer", "Classic, Epic", -800, "Greek", "The Greek hero Odysseus' journey home after the fall of Troy."),
        ("War and Peace", "book", "Leo Tolstoy", "Historical, Fiction", 1869, "Russian", "Broadly focuses on Napoleon's invasion of Russia in 1812 and follows three of the most well-known characters in literature."),
        ("Hamlet", "book", "William Shakespeare", "Drama, Play", 1603, "English", "Prince Hamlet creates a plan to revenge his father's death upon his uncle Claudius."),
        ("Moby Dick", "book", "Herman Melville", "Adventure, Fiction", 1851, "English", "The narrative of Captain Ahab's obsessive quest to kill the giant white whale, Moby Dick."),
        ("The Divine Comedy", "book", "Dante Alighieri", "Epic, Poetry", 1320, "Italian", "Dante's journey through Hell, Purgatory, and Paradise."),
        ("The Brothers Karamazov", "book", "Fyodor Dostoevsky", "Philosophical, Fiction", 1880, "Russian", "The story of Fyodor Karamazov and his three sons—Dmitri, Ivan, and Alyosha."),
        ("Anna Karenina", "book", "Leo Tolstoy", "Romance, Fiction", 1877, "Russian", "The tragic story of Countess Anna Karenina, a married noblewoman and socialite, and her affair with the affluent Count Vronsky."),
        ("Brave New World", "book", "Aldous Huxley", "Dystopian, Sci-Fi", 1932, "English", "A dystopian social science fiction novel that anticipates huge scientific advancements in reproductive technology, sleep-learning, psychological manipulation and classical conditioning."),
        ("Wuthering Heights", "book", "Emily Brontë", "Gothic, Fiction", 1847, "English", "The intense and demonic love between Catherine Earnshaw and Heathcliff."),
        ("Frankenstein", "book", "Mary Shelley", "Horror, Sci-Fi", 1818, "English", "Victor Frankenstein, a young scientist who creates a sapient creature in an unorthodox scientific experiment."),
        ("Alice's Adventures in Wonderland", "book", "Lewis Carroll", "Fantasy, Fiction", 1865, "English", "A young girl named Alice falls through a rabbit hole into a fantasy world populated by peculiar, anthropomorphic creatures."),
        ("The Picture of Dorian Gray", "book", "Oscar Wilde", "Gothic, Fiction", 1890, "English", "A young man sells his soul to ensure that he will never grow old, while a portrait of him ages and records every sin."),
        ("Catch-22", "book", "Joseph Heller", "Satire, War", 1961, "English", "Captain John Yossarian, a U.S. Army Air Forces B-25 bombardier, and his attempts to keep his sanity while fulfilling his service requirements so that he may go home."),
        ("The Stranger", "book", "Albert Camus", "Philosophy, Fiction", 1942, "French", "An ordinary man is unwittingly drawn into a senseless murder on an Algerian beach."),
        ("Heart of Darkness", "book", "Joseph Conrad", "Adventure, Fiction", 1899, "English", "Charles Marlow's voyage up the Congo River in the Congo Free State in the so-called 'Heart of Africa'."),
        ("Gulliver's Travels", "book", "Jonathan Swift", "Satire, Fantasy", 1726, "English", "The voyages of Lemuel Gulliver to several remote nations of the world."),
        ("Les Misérables", "book", "Victor Hugo", "Historical, Drama", 1862, "French", "The story of Jean Valjean, a French peasant, and his desire for redemption after serving nineteen years in jail for stealing a loaf of bread."),
        ("The Grapes of Wrath", "book", "John Steinbeck", "Historical, Fiction", 1939, "English", "The Joads, a poor family of tenant farmers, driven from their Oklahoma home by drought, economic hardship, agricultural industry changes, and bank foreclosures."),
        ("Of Mice and Men", "book", "John Steinbeck", "Drama, Fiction", 1937, "English", "George Milton and Lennie Small, two displaced migrant ranch workers, who move from place to place in California in search of new job opportunities during the Great Depression."),
        ("A Game of Thrones", "book", "George R.R. Martin", "Fantasy, Fiction", 1996, "English", "Several noble houses fight a civil war over who should be king, while an exiled princess plans to return and reclaim her throne, and a supernatural threat rises in the North."),
        ("The Shining", "book", "Stephen King", "Horror, Thriller", 1977, "English", "Jack Torrance's new job at the Overlook Hotel is the perfect chance for a fresh start. As the harsh winter weather sets in, the idyllic location feels ever more remote."),
        ("It", "book", "Stephen King", "Horror, Thriller", 1986, "English", "The story of seven children in Derry, Maine, who are terrorized by the eponymous being, only to face the monster again in later life."),
        ("The Hunger Games", "book", "Suzanne Collins", "Dystopian, Sci-Fi", 2008, "English", "In the ruins of a place once known as North America lies the nation of Panem, a shining Capitol surrounded by twelve outlying districts."),
    ]
    
    new_items = []
    for item in items_source:
        if item[0] not in existing_titles:
            new_items.append({
                "title": item[0],
                "type": item[1],
                "author_or_director": item[2],
                "genres": item[3],
                "year": item[4],
                "language": item[5],
                "description": item[6],
                "availability_status": random.choice(["Available", "Issued", "Reference"]),
                "cover_image_url": get_cover(item[0], item[1])
            })
            existing_titles.add(item[0]) # Avoid duplicates within the loop

    for item_data in new_items:
        db_item = models.Item(**item_data)
        db.add(db_item)
    
    db.commit()
    print(f"Added {len(new_items)} new items with images!")

if __name__ == "__main__":
    seed()
