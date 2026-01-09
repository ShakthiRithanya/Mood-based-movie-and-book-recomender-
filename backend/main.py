from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, auth, database, recommendation
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library/Hostel Recommender")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except auth.JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@app.on_event("startup")
def startup_event():
    db = database.SessionLocal()
    recommendation.recommender.load_data(db)
    db.close()

@app.post("/auth/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@app.get("/items", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, search: str = None, type: str = None, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit, search=search, type=type)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    item_obj = crud.create_item(db=db, item=item)
    # Trigger retrain (simple approach for now)
    try:
        recommendation.recommender.load_data(db)
    except:
        pass
    return item_obj

@app.post("/ratings", response_model=schemas.Rating)
def rate_item(rating: schemas.RatingCreate, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_rating(db=db, rating=rating, user_id=current_user.id)

@app.get("/recommendations/item/{item_id}", response_model=List[schemas.Item])
def get_similar_items(item_id: int, db: Session = Depends(get_db)):
    ids = recommendation.recommender.get_similar_items(item_id)
    return db.query(models.Item).filter(models.Item.id.in_(ids)).all()

@app.get("/recommendations/mood", response_model=List[schemas.Item])
def get_mood_recommendations(mood: str, db: Session = Depends(get_db)):
    if mood not in recommendation.recommender.mood_map:
         raise HTTPException(status_code=400, detail="Invalid mood")
    
    ids = recommendation.recommender.get_recommendations_by_mood(mood)
    return db.query(models.Item).filter(models.Item.id.in_(ids)).all()

@app.get("/recommendations/user", response_model=List[schemas.Item])
def get_user_recommendations(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    ids = recommendation.recommender.get_user_recommendations(current_user.id, db)
    return db.query(models.Item).filter(models.Item.id.in_(ids)).all()
