import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from . import models
import random

class Recommender:
    def __init__(self):
        self.similarity_matrix = None
        self.items_df = None
        self.indices = None
        
        # Mood to Genre/Keyword Mapping
        self.mood_map = {
            "Happy": ["Comedy", "Animation", "Family", "Adventure", "Musical", "Romance"],
            "Sad": ["Drama", "Romance", "War", "Tragedy"],
            "Excited": ["Action", "Thriller", "Sci-Fi", "Crime", "Adventure"],
            "Chill": ["Fantasy", "History", "Biography", "Classic", "Philosophy"],
            "Scared": ["Horror", "Mystery", "Thriller", "Crime", "Gothic"],
            "Inspired": ["Biography", "Sport", "Drama", "History", "Non-fiction"]
        }

    def load_data(self, db: Session):
        items = db.query(models.Item).all()
        if not items:
            return
        
        data = []
        for item in items:
            data.append({
                "id": item.id,
                "title": item.title,
                "genres": item.genres,
                "description": item.description,
                "soup": (item.genres or "") + " " + (item.description or "")
            })
        
        self.items_df = pd.DataFrame(data)
        self.items_df['soup'] = self.items_df['soup'].fillna('')
        
        # We can keep the basic TF-IDF for "Similar Items" logic
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.items_df['soup'])
        
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        self.indices = pd.Series(self.items_df.index, index=self.items_df['id']).drop_duplicates()
        print("Recommender system retrained.")

    def get_similar_items(self, item_id: int, top_n: int = 5):
        if self.similarity_matrix is None or item_id not in self.indices:
            return []
            
        idx = self.indices[item_id]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        item_indices = [i[0] for i in sim_scores]
        return self.items_df['id'].iloc[item_indices].tolist()

    def get_user_recommendations(self, user_id: int, db: Session, top_n: int = 5):
        # Existing logic... keeping strictly for legacy or "Similar to what you liked"
        ratings = db.query(models.Rating).filter(models.Rating.user_id == user_id, models.Rating.rating >= 4).all()
        if not ratings:
            return [item.id for item in db.query(models.Item).limit(top_n).all()]
        
        candidates = {}
        for r in ratings:
            sim_ids = self.get_similar_items(r.item_id, top_n=5)
            for sim_id in sim_ids:
                candidates[sim_id] = candidates.get(sim_id, 0) + 1
        
        rated_items = {r.item_id for r in db.query(models.Rating).filter(models.Rating.user_id == user_id).all()}
        final_recs = [iid for iid, score in sorted(candidates.items(), key=lambda x: x[1], reverse=True) if iid not in rated_items]
        
        return final_recs[:top_n]

    def get_recommendations_by_mood(self, mood: str, top_n: int = 10):
        if self.items_df is None or mood not in self.mood_map:
            return []

        target_genres = self.mood_map[mood]
        
        # Simple Filter: Check if item genres contain any of the target genres
        # Scoring: +1 for each matching genre
        
        def score_item(row):
            score = 0
            item_genres = (row['genres'] or "").split(', ')
            for g in item_genres:
                # Partial match allowed (e.g. "Sci-Fi" matches "Sci-Fi")
                for target in target_genres:
                    if target.lower() in g.lower():
                        score += 1
            return score

        # Create a copy to not affect global state
        temp_df = self.items_df.copy()
        temp_df['mood_score'] = temp_df.apply(score_item, axis=1)
        
        # Filter items with at least one match
        mood_items = temp_df[temp_df['mood_score'] > 0]
        
        if mood_items.empty:
            return []
            
        # Sort by score (descending) and then randomize slightly for variety within top matches
        # We take top 20 matches, then shuffle and return N to give variety on refresh
        top_matches = mood_items.sort_values('mood_score', ascending=False).head(top_n * 3)
        
        recommendations = top_matches.sample(min(len(top_matches), top_n)).index.tolist()
        
        # Map DataFrame Index back to Item ID
        # Note: self.items_df index might need specific mapping if it wasn't 0..N
        # But we built it from list, so iloc logic works, but let's be safe:
        return top_matches.loc[recommendations]['id'].tolist()

recommender = Recommender()
