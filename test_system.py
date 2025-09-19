import requests
import time
import subprocess
import sys

def test_api():
    """Test API endpoints"""
    base_url = "http://localhost:8000"
    
    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: {response.status_code}")
        
        # Test movies endpoint
        response = requests.get(f"{base_url}/movies")
        print(f"Movies endpoint: {response.status_code}")
        
        if response.status_code == 200:
            movies = response.json()["movies"]
            print(f"Found {len(movies)} movies")
            
            # Test recommendations
            liked_movies = [movies[0]["movie_id"], movies[1]["movie_id"]]
            response = requests.post(
                f"{base_url}/recommend",
                json=liked_movies,
                params={"n_recommendations": 5}
            )
            print(f"Recommendations endpoint: {response.status_code}")
            
            if response.status_code == 200:
                recommendations = response.json()["recommendations"]
                print(f"Got {len(recommendations)} recommendations")
                for rec in recommendations:
                    print(f"  - {rec['title']} (score: {rec['similarity_score']:.3f})")
        
    except requests.exceptions.RequestException as e:
        print(f"API test failed: {e}")

if __name__ == "__main__":
    print("Testing Movie Recommendation System...")
    test_api()