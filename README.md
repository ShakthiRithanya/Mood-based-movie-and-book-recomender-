# LibRec: Book & Movie Recommendation System

A full-stack AI/ML mini project for College Hostel Library.

## Features
- **Student & Admin Portals**: Role-based authentication.
- **Catalog Management**: Admin can add books and movies.
- **Recommendation Engine**: Content-based filtering using TF-IDF and Cosine Similarity.
- **Interactive UI**: Modern, premium glassmorphism design using React.
- **User Dashboard**: Personalized recommendations based on ratings.

## Tech Stack
- **Frontend**: React, Vite, CSS Modules (Premium Dark Theme)
- **Backend**: FastAPI (Python), SQLAlchemy
- **Database**: SQLite (local `app.db`)
- **ML**: scikit-learn (TF-IDF)

## Setup instructions

### Backend
1. Open a terminal in the root directory.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Seed the database (optional, runs once):
   ```bash
   python -m backend.seed
   ```
4. Start the server:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```
   Server runs on `http://localhost:8000`.

### Frontend
1. Open a terminal in `frontend/` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```
4. Open `http://localhost:5173`.

## Usage
- **Login**: 
  - Student: `student@college.edu` / `123` (or similar if seeded, default seed user is `student@college.edu` / `student123`)
  - Admin: `admin@college.edu` / `admin123`
- **Rate Items**: Go to catalog, click an item, give it stars.
- **Recommendations**: Check your dashboard after rating items.

## Recommendation Logic
The system combines item genres and descriptions into a "soup" of text. It uses TF-IDF Vectorizer to convert this text into numerical vectors and calculates Cosine Similarity between all items. When a user rates an item highly, the system suggests items that are most similar to it.
