import random
import urllib.parse
from backend.database import SessionLocal
from backend import models
from backend.auth import get_password_hash

db = SessionLocal()

def seed_more():
    existing_titles = {item.title for item in db.query(models.Item).all()}
    
    # ---------------------------------------------------------
    # 1. BOOKS (OpenLibrary is reliable for these)
    # ---------------------------------------------------------
    books_source = [
        ("The Handmaid's Tale", "Margaret Atwood", "Dystopian, Sci-Fi", 1985, "English", "Offred is a Handmaid in the Republic of Gilead, a totalitarian and theocratic state."),
        ("Life of Pi", "Yann Martel", "Adventure, Fiction", 2001, "English", "The surviving string of a shipwreck, a teenage boy named Pi, finds himself on a lifeboat with a Bengal tiger."),
        ("A Thousand Splendid Suns", "Khaled Hosseini", "Historical, Fiction", 2007, "English", "A breathtaking story set against the volatile events of Afghanistan's last thirty years."),
        ("Gone Girl", "Gillian Flynn", "Thriller, Mystery", 2012, "English", "On her fifth wedding anniversary, Nick Dunne reports that his beautiful wife, Amy, has gone missing."),
        ("The Girl on the Train", "Paula Hawkins", "Thriller, Mystery", 2015, "English", "Rachel Watson catches daily glimpses of a seemingly perfect couple from the window of the train she takes to work."),
        ("The Help", "Kathryn Stockett", "Historical, Fiction", 2009, "English", "African Americans working in white households in Jackson, Mississippi, during the early 1960s."),
        ("Percy Jackson & The Olympians: The Lightning Thief", "Rick Riordan", "Fantasy, Adventure", 2005, "English", "Percy Jackson discovers he is a demigod and is accused of stealing Zeus' lightning bolt."),
        ("Divergent", "Veronica Roth", "Dystopian, YA", 2011, "English", "In a world divided by factions based on virtues, Tris learns she's Divergent and won't fit in."),
        ("The Maze Runner", "James Dashner", "Dystopian, Sci-Fi", 2009, "English", "Thomas wakes up in a lift with no memory of who he is, only to find himself in the Glade."),
        ("Twilight", "Stephenie Meyer", "Fantasy, Romance", 2005, "English", "Bella Swan moves to Forks and falls in love with Edward Cullen, a vampire."),
        ("The Fault in Our Stars", "John Green", "Romance, YA", 2012, "English", "Hazel and Gus are two teenagers who share an acerbic wit, a disdain for the conventional, and a love that sweeps them on a journey."),
        ("The Giver", "Lois Lowry", "Dystopian, Sci-Fi", 1993, "English", "Jonas lives in a seemingly ideal, if colorless, world of conformity and contentment."),
        ("Holes", "Louis Sachar", "Adventure, Fiction", 1998, "English", "Stanley Yelnats is sent to a correctional boot camp at Camp Green Lake."),
        ("Coraline", "Neil Gaiman", "Fantasy, Horror", 2002, "English", "Coraline ventures through a mysterious door into a world that is similar, yet disturbingly different from her own."),
        ("Wonder", "R.J. Palacio", "Fiction, Drama", 2012, "English", "August Pullman creates a ripple effect in his community as he enters fifth grade."),
        ("Matilda", "Roald Dahl", "Fantasy, Children", 1988, "English", "Matilda involves a precocious child with telekinetic powers who deals with her parents and the tyrannical principal."),
        ("Charlotte's Web", "E.B. White", "Children, Classic", 1952, "English", "The story of a pig named Wilbur and his friendship with a barn spider named Charlotte."),
        ("Dracula", "Bram Stoker", "Horror, Classic", 1897, "English", "The vampire Count Dracula's attempt to move from Transylvania to England."),
        ("Dr. Jekyll and Mr. Hyde", "Robert Louis Stevenson", "Horror, Sci-Fi", 1886, "English", "A London legal practitioner investigates strange occurrences between his old friend, Dr. Henry Jekyll, and the evil Edward Hyde."),
        ("The War of the Worlds", "H.G. Wells", "Sci-Fi, Classic", 1898, "English", "A plot that chronicles the events of a Martian invasion of Earth."),
        ("The Time Machine", "H.G. Wells", "Sci-Fi, Classic", 1895, "English", "A Victorian scientist creates a machine that allows him to travel into the future."),
        ("The Invisible Man", "H.G. Wells", "Sci-Fi, Horror", 1897, "English", "A scientist who has dedicated his life to research into optics and invents a way to change a body's refractive index."),
        ("Great Expectations", "Charles Dickens", "Classic, Fiction", 1861, "English", "The personal growth and personal development of an orphan nicknamed Pip."),
        ("David Copperfield", "Charles Dickens", "Classic, Fiction", 1850, "English", "The journey of David Copperfield as he navigates a life of poverty and wealth."),
        ("Oliver Twist", "Charles Dickens", "Classic, Fiction", 1838, "English", "The story of the orphan Oliver Twist, born in a workhouse and sold into apprenticeship with an undertaker."),
        ("A Christmas Carol", "Charles Dickens", "Classic, Fantasy", 1843, "English", "Ebenezer Scrooge, an elderly miser, is visited by the ghost of his former business partner Jacob Marley."),
        ("Emma", "Jane Austen", "Romance, Classic", 1815, "English", "Emma Woodhouse is a young woman who occupies herself with matchmaking."),
        ("Sense and Sensibility", "Jane Austen", "Romance, Classic", 1811, "English", "Depending on the time, place and other specific factors, the Dashwood sisters' lives are changed."),
        ("Persuasion", "Jane Austen", "Romance, Classic", 1817, "English", "Anne Elliot is a young Englishwoman of 27 years, whose family is moving to lower their expenses."),
        ("Memoirs of a Geisha", "Arthur Golden", "Historical, Fiction", 1997, "English", "A literary sensation and runaway bestseller, this brilliant debut novel tells with seamless authenticity and exquisite lyricism the true confessions of one of Japan's most celebrated geisha."),
        ("Water for Elephants", "Sara Gruen", "Historical, Romance", 2006, "English", "Jacob Jankowski, recently orphaned and adrift, jumps onto a passing train, entering a world of freaks, drifters, and misfits."),
        ("Ready Player One", "Ernest Cline", "Sci-Fi, Adventure", 2011, "English", "In the year 2045, reality is an ugly place. The only time Wade Watts really feels alive is when he's jacked into the OASIS."),
        ("Ender's Game", "Orson Scott Card", "Sci-Fi, Action", 1985, "English", "Andrew 'Ender' Wiggin thinks he is playing computer simulated war games; he is, in fact, engaged in something far more desperate."),
        ("The Martian", "Andy Weir", "Sci-Fi, Adventure", 2011, "English", "Six days ago, astronaut Mark Watney became one of the first people to walk on Mars. Now, he's sure he'll be the first person to die there."),
        ("Jurassic Park", "Michael Crichton", "Sci-Fi, Thriller", 1990, "English", "An island theme park populated by cloned dinosaurs involves a tour group that fights for survival."),
        ("The Green Mile", "Stephen King", "Fantasy, Crime", 1996, "English", "At Cold Mountain Penitentiary, along the mile of green linoleum floor, Paul Edgecombe watches as the new prisoner arrives."),
        ("Misery", "Stephen King", "Horror, Thriller", 1987, "English", "Paul Sheldon is a famous writer who is rescued from a car crash by his number one fan."),
        ("Pet Sematary", "Stephen King", "Horror, Thriller", 1983, "English", "The Creeds are a loving family, but the woods behind their new home hold a blood-chilling secret."),
        ("Carrie", "Stephen King", "Horror, Thriller", 1974, "English", "Styles of epistolary novel, non-linear narrative, 1970s high school setting."),
        ("Lolita", "Vladimir Nabokov", "Classic, Drama", 1955, "English", "Humbert Humbert, a literature professor, becomes obsessed with a 12-year-old girl."),
        ("Beloved", "Toni Morrison", "Historical, Fiction", 1987, "English", "Set after the American Civil War, it is inspired by the story of an African-American slave, Margaret Garner."),
        ("The Color Purple", "Alice Walker", "Historical, Fiction", 1982, "English", "The life of African-American women in the Southern United States in the 1930s."),
        ("Things Fall Apart", "Chinua Achebe", "Historical, Fiction", 1958, "English", "The life of Okonkwo, an Igbo leader and local wrestling champion in the fictional Nigerian village of Umuofia."),
        ("One Hundred Years of Solitude", "Gabriel García Márquez", "Magical Realism", 1967, "Spanish", "The multi-generational story of the Buendía family, whose patriarch, José Arcadio Buendía, founds the town of Macondo."),
        ("Fight Club", "Chuck Palahniuk", "Fiction, Satire", 1996, "English", "An insomniac office worker looking for a way to change his life crosses paths with a devil-may-care soap maker."),
        ("American Psycho", "Bret Easton Ellis", "Horror, Satire", 1991, "English", "Patrick Bateman is twenty-six and he works on Wall Street, he is handsome, sophisticated, charming and intelligent. He is also a psychopath."),
        ("A Clockwork Orange", "Anthony Burgess", "Dystopian, Sci-Fi", 1962, "English", "Set in a near-future English city, it features a teenage protagonist, Alex, who narrates his violent exploits."),
        ("Trainspotting", "Irvine Welsh", "Fiction, Drama", 1993, "English", "A collection of short stories revolving around various residents of Leith, Edinburgh, who use heroin."),
        ("No Country for Old Men", "Cormac McCarthy", "Thriller, Western", 2005, "English", "Llewelyn Moss finds a pickup truck surrounded by a bodyguard of dead men."),
        ("The Road", "Cormac McCarthy", "Post-Apocalyptic, Fiction", 2006, "English", "A father and his young son journey across a burned America."),
    ]

    # ---------------------------------------------------------
    # 2. MOVIES (Mapping common ones to Wikimedia/Images)
    # ---------------------------------------------------------
    # We will accept that some might fall back to the aesthetic Picsum, but we try hard.
    movies_source = [
        ("Jurassic Park", "Steven Spielberg", "Adventure, Sci-Fi", 1993, "English", "A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park's cloned dinosaurs to run loose.", "https://upload.wikimedia.org/wikipedia/en/e/e7/Jurassic_Park_poster.jpg"),
        ("The Batman", "Matt Reeves", "Action, Crime, Drama", 2022, "English", "When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption.", "https://upload.wikimedia.org/wikipedia/en/f/ff/The_Batman_%28film%29_poster.jpg"),
        ("Avengers: Endgame", "Anthony Russo", "Action, Adventure, Sci-Fi", 2019, "English", "After the devastating events of Infinity War, the universe is in ruins. The Avengers assemble once more in order to reverse Thanos' actions.", "https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg"),
        ("Spider-Man: Into the Spider-Verse", "Bob Persichetti", "Animation, Action", 2018, "English", "Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions.", "https://upload.wikimedia.org/wikipedia/en/f/fa/Spider-Man_Into_the_Spider-Verse_poster.png"),
        ("The Dark Knight Rises", "Christopher Nolan", "Action, Thriller", 2012, "English", "Eight years after the Joker's reign of anarchy, Batman, with the help of the enigmatic Catwoman, is forced from his exile to save Gotham City.", "https://upload.wikimedia.org/wikipedia/en/8/83/Dark_knight_rises_poster.jpg"),
        ("Coco", "Lee Unkrich", "Animation, Adventure", 2017, "English", "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather.", "https://upload.wikimedia.org/wikipedia/en/9/98/Coco_%282017_film%29_poster.jpg"),
        ("WALL-E", "Andrew Stanton", "Animation, Adventure", 2008, "English", "In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will ultimately decide the fate of mankind.", "https://upload.wikimedia.org/wikipedia/en/c/c2/WALL-Eposter.jpg"),
        ("Up", "Pete Docter", "Animation, Adventure", 2009, "English", "78-year-old Carl Fredricksen travels to Paradise Falls in his house equipped with balloons, inadvertently taking a young stowaway.", "https://upload.wikimedia.org/wikipedia/en/0/05/Up_%282009_film%29.jpg"),
        ("Toy Story", "John Lasseter", "Animation, Comedy", 1995, "English", "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room.", "https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg"),
        ("The Truman Show", "Peter Weir", "Comedy, Drama", 1998, "English", "An insurance salesman discovers his whole life is actually a reality TV show.", "https://upload.wikimedia.org/wikipedia/en/c/cd/Trumanshow.jpg"),
        ("Blade Runner 2049", "Denis Villeneuve", "Action, Sci-Fi", 2017, "English", "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years.", "https://upload.wikimedia.org/wikipedia/en/9/9b/Blade_Runner_2049_poster.png"),
        ("Mad Max: Fury Road", "George Miller", "Action, Adventure", 2015, "English", "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max.", "https://upload.wikimedia.org/wikipedia/en/6/6e/Mad_Max_Fury_Road.jpg"),
        ("Get Out", "Jordan Peele", "Horror, Mystery", 2017, "English", "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point.", "https://upload.wikimedia.org/wikipedia/en/a/a3/Get_Out_poster.png"),
        ("Moonlight", "Barry Jenkins", "Drama", 2016, "English", "A young African-American man grapples with his identity and sexuality while experiencing the everyday struggles of childhood, adolescence, and burgeoning adulthood.", "https://upload.wikimedia.org/wikipedia/en/8/84/Moonlight_%282016_film%29_poster.jpg"),
        ("Her", "Spike Jonze", "Drama, Romance, Sci-Fi", 2013, "English", "In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need.", "https://upload.wikimedia.org/wikipedia/en/4/44/Her2013Poster.jpg"),
        ("Ex Machina", "Alex Garland", "Drama, Sci-Fi", 2014, "English", "A young programmer is selected to participate in a ground-breaking experiment in synthetic intelligence by evaluating the human qualities of a highly advanced humanoid A.I.", "https://upload.wikimedia.org/wikipedia/en/b/ba/Ex-machina-uk-poster.jpg"),
        ("Arrival", "Denis Villeneuve", "Drama, Sci-Fi", 2016, "English", "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.", "https://upload.wikimedia.org/wikipedia/en/d/df/Arrival_2016_film_poster.jpg"),
        ("A Quiet Place", "John Krasinski", "Drama, Horror", 2018, "English", "In a post-apocalyptic world, a family is forced to live in silence while hiding from monsters with ultra-sensitive hearing.", "https://upload.wikimedia.org/wikipedia/en/a/a0/A_Quiet_Place_film_poster.png"),
        ("Black Panther", "Ryan Coogler", "Action, Adventure", 2018, "English", "T'Challa, heir to the hidden but advanced kingdom of Wakanda, must step forward to lead his people into a new future and must confront a challenger from his country's past.", "https://upload.wikimedia.org/wikipedia/en/d/d6/Black_Panther_%28film%29_poster.jpg"),
        ("Logan", "James Mangold", "Action, Drama", 2017, "English", "In a future where mutants are nearly extinct, an elderly and weary Logan leads a quiet life. But when Laura, a mutant child pursued by scientists, comes to him for help, he must get her to safety.", "https://upload.wikimedia.org/wikipedia/en/3/37/Logan_2017_poster.jpg"),
        ("Deadpool", "Tim Miller", "Action, Comedy", 2016, "English", "A wisecracking mercenary gets experimented on and becomes immortal but ugly, and sets out to track down the man who ruined his looks.", "https://upload.wikimedia.org/wikipedia/en/2/23/Deadpool_%282016_poster%29.png"),
        ("Guardians of the Galaxy", "James Gunn", "Action, Adventure", 2014, "English", "A group of intergalactic criminals must pull together to stop a fanatical warrior with plans to purge the universe.", "https://upload.wikimedia.org/wikipedia/en/3/33/Guardians_of_the_Galaxy_%28film%29_poster.jpg"),
        ("Wonder Woman", "Patty Jenkins", "Action, Adventure", 2017, "English", "When a pilot crashes and tells of conflict in the outside world, Diana, an Amazonian warrior in training, leaves home to fight a war, discovering her full powers and true destiny.", "https://upload.wikimedia.org/wikipedia/en/e/ed/Wonder_Woman_%282017_film%29.jpg"),
        ("12 Angry Men", "Sidney Lumet", "Crime, Drama", 1957, "English", "The jury in a New York City murder trial is frustrated by a single member whose skeptical caution forces them to more carefully consider the evidence before jumping to a hasty verdict.", "https://upload.wikimedia.org/wikipedia/commons/b/b5/12_Angry_Men_%281957_film_poster%29.jpg"),
        ("Rear Window", "Alfred Hitchcock", "Mystery, Thriller", 1954, "English", "A wheelchair-bound photographer spies on his neighbors from his apartment window and becomes convinced one of them has committed murder.", "https://upload.wikimedia.org/wikipedia/commons/3/38/Rear_Window_film_poster.jpg"),
        ("North by Northwest", "Alfred Hitchcock", "Action, Adventure, Mystery", 1959, "English", "A New York City advertising executive goes on the run after being mistaken for a government agent by a group of foreign spies.", "https://upload.wikimedia.org/wikipedia/commons/8/83/North_by_Northwest_%281959%29_poster.png"),
        ("2001: A Space Odyssey", "Stanley Kubrick", "Sci-Fi, Adventure", 1968, "English", "After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer H.A.L. 9000.", "https://upload.wikimedia.org/wikipedia/en/a/a7/2001_A_Space_Odyssey_%281968%29_theatrical_poster.jpg"),
        ("A Clockwork Orange", "Stanley Kubrick", "Crime, Sci-Fi", 1971, "English", "In the future, a sadistic gang leader is imprisoned and volunteers for a conduct-aversion experiment, but it doesn't go as planned.", "https://upload.wikimedia.org/wikipedia/en/4/48/Clockwork_orange_ver2.jpg"),
        ("Full Metal Jacket", "Stanley Kubrick", "Drama, War", 1987, "English", "A pragmatic U.S. Marine observes the dehumanizing effects the Vietnam War has on his fellow recruits from their brutal boot camp training to the bloody street fighting in Hue.", "https://upload.wikimedia.org/wikipedia/en/9/99/Full_Metal_Jacket_poster.jpg"),
        ("Taxi Driver", "Martin Scorsese", "Crime, Drama", 1976, "English", "A mentally unstable veteran works as a nighttime taxi driver in New York City, where the perceived decadence and sleaze fuels his urge for violent action.", "https://upload.wikimedia.org/wikipedia/en/3/33/Taxi_Driver_%281976_film_poster%29.jpg"),
        ("Apocalypse Now", "Francis Ford Coppola", "Drama, Mystery, War", 1979, "English", "A U.S. Army officer serving in Vietnam is tasked with assassinating a renegade Special Forces Colonel who sees himself as a god.", "https://upload.wikimedia.org/wikipedia/en/c/c2/Apocalypse_Now_poster.jpg"),
        ("Alien", "Ridley Scott", "Horror, Sci-Fi", 1979, "English", "After a space merchant vessel receives an unknown transmission as a distress call, one of the crew is attacked by a mysterious life form.", "https://upload.wikimedia.org/wikipedia/en/c/c3/Alien_movie_poster.jpg"),
        ("Aliens", "James Cameron", "Action, Adventure", 1986, "English", "Fifty-seven years after surviving an apocalyptic attack aboard her space vessel by merciless space creatures, Officer Ripley awakens from hyper-sleep and tries to warn anyone who will listen about the predators.", "https://upload.wikimedia.org/wikipedia/en/f/fb/Aliens_poster.jpg"),
        ("Terminator 2: Judgment Day", "James Cameron", "Action, Sci-Fi", 1991, "English", "A cyborg, identical to the one who failed to kill Sarah Connor, must now protect her ten-year-old son, John, from a more advanced and powerful cyborg.", "https://upload.wikimedia.org/wikipedia/en/8/85/Terminator2poster.jpg"),
        ("The Prestige", "Christopher Nolan", "Drama, Mystery", 2006, "English", "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other.", "https://upload.wikimedia.org/wikipedia/en/d/d2/Prestige_poster.jpg"),
        ("Memento", "Christopher Nolan", "Mystery, Thriller", 2000, "English", "A man with short-term memory loss attempts to track down his wife's murderer.", "https://upload.wikimedia.org/wikipedia/en/c/c7/Memento_poster.jpg"),
        ("Shutter Island", "Martin Scorsese", "Mystery, Thriller", 2010, "English", "In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.", "https://upload.wikimedia.org/wikipedia/en/7/76/Shutter_Island_%282010%29_poster.jpg"),
        ("The Wolf of Wall Street", "Martin Scorsese", "Biography, Comedy, Crime", 2013, "English", "Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker living the high life to his fall involving crime, corruption and the federal government.", "https://upload.wikimedia.org/wikipedia/en/1/1f/WallStreet2013poster.jpg"),
        ("Django Unchained", "Quentin Tarantino", "Drama, Western", 2012, "English", "With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal plantation-owner in Mississippi.", "https://upload.wikimedia.org/wikipedia/en/8/8b/Django_Unchained_Poster.jpg"),
        ("Inglourious Basterds", "Quentin Tarantino", "Adventure, Drama, War", 2009, "English", "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group of Jewish U.S. soldiers coincides with a theatre owner's vengeful plans.", "https://upload.wikimedia.org/wikipedia/en/c/c3/Inglourious_Basterds_poster.jpg"),
        ("Reservoir Dogs", "Quentin Tarantino", "Crime, Drama", 1992, "English", "When a simple jewelry heist goes horribly wrong, the surviving criminals begin to suspect that one of them is a police informant.", "https://upload.wikimedia.org/wikipedia/en/f/f3/Reservoir_Dogs.jpg"),
        ("Oldboy", "Park Chan-wook", "Action, Drama", 2003, "Korean", "After being kidnapped and imprisoned for fifteen years, Oh Dae-Su is released, only to find that he must find his captor in five days.", "https://upload.wikimedia.org/wikipedia/en/6/67/Oldboykoreanposter.jpg"),
        ("Train to Busan", "Yeon Sang-ho", "Action, Horror", 2016, "Korean", "While a zombie virus breaks out in South Korea, passengers struggle to survive on the train from Seoul to Busan.", "https://upload.wikimedia.org/wikipedia/en/9/95/Train_to_Busan.jpg"),
        ("Your Name", "Makoto Shinkai", "Animation, Drama", 2016, "Japanese", "Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart?", "https://upload.wikimedia.org/wikipedia/en/0/0b/Your_Name_poster.png"),
        ("Howl's Moving Castle", "Hayao Miyazaki", "Animation, Adventure", 2004, "Japanese", "When an unconfident young woman is cursed with an old body by a spiteful witch, her only chance of breaking the spell lies with a self-indulgent yet insecure young wizard and his companions in his legged, walking castle.", "https://upload.wikimedia.org/wikipedia/en/a/a0/Howls-moving-castleposter.jpg"),
        ("Princess Mononoke", "Hayao Miyazaki", "Animation, Adventure", 1997, "Japanese", "On a journey to find the cure for a Tatarigami's curse, Ashitaka finds himself in the middle of a war between the forest gods and Tatara, a mining colony.", "https://upload.wikimedia.org/wikipedia/en/8/8c/Princess_Mononoke_Japanese_poster.png"),
        ("My Neighbor Totoro", "Hayao Miyazaki", "Animation, Family", 1988, "Japanese", "When two girls move to the country to be near their ailing mother, they have adventures with the wondrous forest spirits who live nearby.", "https://upload.wikimedia.org/wikipedia/en/0/02/My_Neighbor_Totoro_-_Tonari_no_Totoro_%28Movie_Poster%29.jpg"),
        ("Akira", "Katsuhiro Otomo", "Animation, Action", 1988, "Japanese", "A secret military project endangers Neo-Tokyo when it turns a biker gang member into a rampaging psychic psychopath who can only be stopped by two teenagers and a group of psychics.", "https://upload.wikimedia.org/wikipedia/en/5/5d/Akira_1988_poster.jpg"),
    ]

    new_items_count = 0
    
    # Process Books
    for b in books_source:
        if b[0] not in existing_titles:
            encoded_title = urllib.parse.quote(b[0].replace(" ", "_"))
            # Force default=false to trigger fallback if missing
            cover_url = f"https://covers.openlibrary.org/b/title/{encoded_title}-L.jpg?default=false"
            
            item = models.Item(
                title=b[0],
                type="book",
                author_or_director=b[1],
                genres=b[2],
                year=b[3],
                language=b[4],
                description=b[5],
                availability_status=random.choice(["Available", "Issued", "Reference"]),
                cover_image_url=cover_url
            )
            db.add(item)
            new_items_count += 1
            existing_titles.add(b[0])

    # Process Movies
    for m in movies_source:
        if m[0] not in existing_titles:
            item = models.Item(
                title=m[0],
                type="movie",
                author_or_director=m[1],
                genres=m[2],
                year=m[3],
                language=m[4],
                description=m[5],
                availability_status=random.choice(["Available", "Issued", "Reference"]),
                cover_image_url=m[6] # We have hardcoded URLs here
            )
            db.add(item)
            new_items_count += 1
            existing_titles.add(m[0])
            
    db.commit()
    print(f"Successfully added {new_items_count} new items (Books & Movies)!")

if __name__ == "__main__":
    seed_more()
