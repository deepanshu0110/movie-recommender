import pandas as pd
import numpy as np
import os

class MovieDataLoader:
    def __init__(self, data_path="data/raw/ml-100k"):
        self.data_path = data_path
        self.movies = None
        self.ratings = None
        self.user_movie_matrix = None
        
    def load_data(self):
        """Load movies and ratings data"""
        try:
            # Load movies
            movies_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 
                          'imdb_url', 'unknown', 'action', 'adventure', 'animation', 
                          'children', 'comedy', 'crime', 'documentary', 'drama', 
                          'fantasy', 'film_noir', 'horror', 'musical', 'mystery', 
                          'romance', 'sci_fi', 'thriller', 'war', 'western']
            
            self.movies = pd.read_csv(
                f"{self.data_path}/u.item", 
                sep='|', 
                names=movies_cols, 
                encoding='latin-1'
            )
            
            # Load ratings
            ratings_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
            self.ratings = pd.read_csv(
                f"{self.data_path}/u.data", 
                sep='\t', 
                names=ratings_cols
            )
            
            print(f"✅ Loaded {len(self.movies)} movies and {len(self.ratings)} ratings")
            return self.movies, self.ratings
            
        except FileNotFoundError as e:
            print(f"❌ Data files not found. Please run 'python download_data.py' first.")
            print(f"Error: {e}")
            return None, None
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None, None
    
    def create_user_movie_matrix(self):
        """Create user-movie interaction matrix"""
        if self.ratings is None:
            print("❌ No ratings data loaded. Call load_data() first.")
            return None
            
        try:
            self.user_movie_matrix = self.ratings.pivot_table(
                index='user_id', 
                columns='movie_id', 
                values='rating'
            ).fillna(0)
            
            print(f"✅ User-movie matrix created: {self.user_movie_matrix.shape}")
            return self.user_movie_matrix
            
        except Exception as e:
            print(f"❌ Error creating user-movie matrix: {e}")
            return None
    
    def get_movie_features(self):
        """Get movie genre features for similarity calculation"""
        if self.movies is None:
            print("❌ No movies data loaded. Call load_data() first.")
            return None
            
        genre_cols = ['unknown', 'action', 'adventure', 'animation', 
                     'children', 'comedy', 'crime', 'documentary', 'drama', 
                     'fantasy', 'film_noir', 'horror', 'musical', 'mystery', 
                     'romance', 'sci_fi', 'thriller', 'war', 'western']
        
        movie_features = self.movies[['movie_id'] + genre_cols].set_index('movie_id')
        return movie_features
    
    def analyze_data(self):
        """Print basic data analysis"""
        if self.movies is None or self.ratings is None:
            print("❌ Data not loaded. Call load_data() first.")
            return
            
        print("\n📊 Dataset Analysis:")
        print(f"   Movies: {len(self.movies)}")
        print(f"   Ratings: {len(self.ratings)}")
        print(f"   Users: {self.ratings['user_id'].nunique()}")
        print(f"   Average rating: {self.ratings['rating'].mean():.2f}")
        
        print("\n📈 Rating distribution:")
        rating_counts = self.ratings['rating'].value_counts().sort_index()
        for rating, count in rating_counts.items():
            print(f"   {rating} stars: {count} ratings")