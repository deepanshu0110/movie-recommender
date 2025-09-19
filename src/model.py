import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class MovieRecommender:
    def __init__(self):
        self.movie_similarity_df = None
        self.movies = None
        self.ratings = None
        
    def fit(self, movies, ratings, user_movie_matrix):
        """Train the recommendation model"""
        print("🤖 Training recommendation model...")
        
        self.movies = movies
        self.ratings = ratings
        
        try:
            # Calculate movie-movie similarity based on user ratings
            # Transpose to get movies as rows, users as columns
            movie_user_matrix = user_movie_matrix.T
            
            print(f"   Computing similarity for {movie_user_matrix.shape[0]} movies...")
            
            # Calculate cosine similarity between movies
            movie_similarity = cosine_similarity(movie_user_matrix)
            
            # Convert to DataFrame for easier handling
            self.movie_similarity_df = pd.DataFrame(
                movie_similarity,
                index=movie_user_matrix.index,
                columns=movie_user_matrix.index
            )
            
            print("✅ Model training completed!")
            return True
            
        except Exception as e:
            print(f"❌ Model training failed: {e}")
            return False
        
    def get_recommendations(self, liked_movie_ids, n_recommendations=10):
        """Get top-N movie recommendations based on liked movies"""
        if self.movie_similarity_df is None:
            raise ValueError("Model not trained yet! Please train the model first.")
        
        if not liked_movie_ids:
            return []
        
        print(f"🔍 Getting recommendations for movies: {liked_movie_ids}")
        
        # Calculate average similarity scores for liked movies
        recommendations = {}
        valid_liked_movies = []
        
        for movie_id in liked_movie_ids:
            if movie_id in self.movie_similarity_df.index:
                valid_liked_movies.append(movie_id)
                similar_movies = self.movie_similarity_df[movie_id].sort_values(ascending=False)
                
                # Add to recommendations (skip the movie itself)
                for sim_movie_id, similarity in similar_movies.items():
                    if sim_movie_id != movie_id and sim_movie_id not in liked_movie_ids:
                        if sim_movie_id not in recommendations:
                            recommendations[sim_movie_id] = []
                        recommendations[sim_movie_id].append(similarity)
            else:
                print(f"⚠️ Movie ID {movie_id} not found in similarity matrix")
        
        if not valid_liked_movies:
            print("❌ None of the provided movie IDs were found")
            return []
        
        # Average the similarity scores
        avg_recommendations = {
            movie_id: np.mean(similarities) 
            for movie_id, similarities in recommendations.items()
        }
        
        # Sort by similarity and get top N
        top_recommendations = sorted(
            avg_recommendations.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n_recommendations]
        
        # Get movie details
        recommended_movies = []
        for movie_id, similarity in top_recommendations:
            movie_row = self.movies[self.movies['movie_id'] == movie_id]
            if not movie_row.empty:
                movie_info = movie_row.iloc[0]
                recommended_movies.append({
                    'movie_id': int(movie_id),
                    'title': movie_info['title'],
                    'similarity_score': float(similarity)
                })
        
        print(f"✅ Found {len(recommended_movies)} recommendations")
        return recommended_movies
    
    def save_model(self, filepath="models/movie_recommender.pkl"):
        """Save the trained model"""
        try:
            os.makedirs("models", exist_ok=True)
            
            model_data = {
                'movie_similarity_df': self.movie_similarity_df,
                'movies': self.movies,
                'ratings': self.ratings
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"✅ Model saved to {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save model: {e}")
            return False
    
    def load_model(self, filepath="models/movie_recommender.pkl"):
        """Load a trained model"""
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Model file not found: {filepath}")
                
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.movie_similarity_df = model_data['movie_similarity_df']
            self.movies = model_data['movies']
            self.ratings = model_data['ratings']
            
            print(f"✅ Model loaded from {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return False
    
    def get_movie_info(self, movie_id):
        """Get information about a specific movie"""
        if self.movies is None:
            return None
            
        movie_row = self.movies[self.movies['movie_id'] == movie_id]
        if movie_row.empty:
            return None
            
        return movie_row.iloc[0].to_dict()
    
    def search_movies(self, search_term):
        """Search for movies by title"""
        if self.movies is None:
            return []
            
        mask = self.movies['title'].str.contains(search_term, case=False, na=False)
        found_movies = self.movies[mask][['movie_id', 'title']].to_dict('records')
        return found_movies