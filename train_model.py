from src.data_loader import MovieDataLoader
from src.model import MovieRecommender
import os

def main():
    print("🎬 Movie Recommendation System - Model Training")
    print("=" * 50)
    
    # Check if data exists
    if not os.path.exists("data/raw/ml-100k"):
        print("❌ MovieLens data not found!")
        print("Please run 'python download_data.py' first to download the dataset.")
        return
    
    try:
        # Initialize data loader
        print("📂 Loading data...")
        loader = MovieDataLoader()
        
        # Load data
        movies, ratings = loader.load_data()
        
        if movies is None or ratings is None:
            print("❌ Failed to load data. Exiting...")
            return
        
        # Analyze data
        loader.analyze_data()
        
        # Create user-movie matrix
        print("\n🔢 Creating user-movie interaction matrix...")
        user_movie_matrix = loader.create_user_movie_matrix()
        
        if user_movie_matrix is None:
            print("❌ Failed to create user-movie matrix. Exiting...")
            return
        
        # Initialize and train model
        print("\n🤖 Training recommendation model...")
        recommender = MovieRecommender()
        
        success = recommender.fit(movies, ratings, user_movie_matrix)
        
        if not success:
            print("❌ Model training failed. Exiting...")
            return
        
        # Save model
        print("\n💾 Saving trained model...")
        success = recommender.save_model()
        
        if success:
            print("\n🎉 Training completed successfully!")
            print("\nNext steps:")
            print("1. Start the API: python run_api.py")
            print("2. Start the dashboard: python run_dashboard.py")
            
            # Test the model with a quick recommendation
            print("\n🧪 Testing model with sample recommendation...")
            try:
                # Get a few popular movies for testing
                sample_movies = [1, 2, 3]  # Toy Story, GoldenEye, Four Weddings and a Funeral
                recommendations = recommender.get_recommendations(sample_movies, 5)
                
                print("Sample recommendations:")
                for i, rec in enumerate(recommendations, 1):
                    print(f"   {i}. {rec['title']} (score: {rec['similarity_score']:.3f})")
                    
            except Exception as e:
                print(f"⚠️ Test failed but model is saved: {e}")
        else:
            print("❌ Failed to save model.")
            
    except Exception as e:
        print(f"❌ Training failed with error: {e}")
        print("Please check your data and try again.")

if __name__ == "__main__":
    main()