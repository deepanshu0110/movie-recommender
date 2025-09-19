import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_dataset(movies, ratings):
    """Analyze the MovieLens dataset"""
    print("=== Dataset Analysis ===")
    print(f"Number of movies: {len(movies)}")
    print(f"Number of ratings: {len(ratings)}")
    print(f"Number of unique users: {ratings['user_id'].nunique()}")
    
    print("\n=== Rating Distribution ===")
    print(ratings['rating'].value_counts().sort_index())
    
    print("\n=== Movies with Most Ratings ===")
    movie_ratings = ratings.groupby('movie_id').size().reset_index(name='rating_count')
    top_movies = movie_ratings.merge(movies[['movie_id', 'title']], on='movie_id')
    print(top_movies.nlargest(10, 'rating_count')[['title', 'rating_count']])

def plot_rating_distribution(ratings):
    """Plot rating distribution"""
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    ratings['rating'].hist(bins=5, edgecolor='black')
    plt.title('Rating Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    
    plt.subplot(1, 2, 2)
    ratings_per_movie = ratings.groupby('movie_id').size()
    plt.hist(ratings_per_movie, bins=50, edgecolor='black')
    plt.title('Number of Ratings per Movie')
    plt.xlabel('Number of Ratings')
    plt.ylabel('Number of Movies')
    
    plt.tight_layout()
    plt.savefig('data/processed/rating_analysis.png')
    plt.show()