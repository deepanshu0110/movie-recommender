from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model import MovieRecommender

app = FastAPI(title="Movie Recommendation API", version="1.0.0")

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
recommender = None

@app.on_event("startup")
async def load_model():
    global recommender
    recommender = MovieRecommender()
    try:
        recommender.load_model("models/movie_recommender.pkl")
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Model not found. Please train the model first.")
        raise HTTPException(status_code=500, detail="Model not available")

@app.get("/")
async def root():
    return {"message": "Movie Recommendation API"}

@app.get("/movies")
async def get_movies():
    """Get all available movies"""
    if recommender is None or recommender.movies is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    movies_list = recommender.movies[['movie_id', 'title']].to_dict('records')
    return {"movies": movies_list}

@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int):
    """Get specific movie details"""
    if recommender is None or recommender.movies is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    movie = recommender.movies[recommender.movies['movie_id'] == movie_id]
    if movie.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return movie.iloc[0].to_dict()

@app.post("/recommend")
async def get_recommendations(liked_movie_ids: List[int], n_recommendations: int = 10):
    """Get movie recommendations based on liked movies"""
    if recommender is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if not liked_movie_ids:
        raise HTTPException(status_code=400, detail="Please provide at least one liked movie")
    
    try:
        recommendations = recommender.get_recommendations(
            liked_movie_ids, 
            n_recommendations
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)