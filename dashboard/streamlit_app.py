import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

API_BASE_URL = "http://localhost:8000"

def load_movies():
    """Load movies from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/movies")
        if response.status_code == 200:
            return response.json()["movies"]
        else:
            st.error("Failed to load movies from API")
            return []
    except requests.exceptions.RequestException:
        st.error("API is not running. Please start the API server first.")
        return []

def get_recommendations(liked_movie_ids, n_recommendations=10):
    """Get recommendations from API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/recommend",
            json=liked_movie_ids,
            params={"n_recommendations": n_recommendations}
        )
        if response.status_code == 200:
            return response.json()["recommendations"]
        else:
            st.error(f"Failed to get recommendations: {response.text}")
            return []
    except requests.exceptions.RequestException:
        st.error("Failed to connect to API")
        return []

def main():
    st.set_page_config(
        page_title="Movie Recommender",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 Movie Recommendation System")
    st.markdown("Select your favorite movies and get personalized recommendations!")
    
    # Load movies
    movies = load_movies()
    
    if not movies:
        st.stop()
    
    # Create movie selection interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Select Your Favorite Movies")
        
        # Create a searchable multiselect
        movie_titles = [f"{movie['title']} (ID: {movie['movie_id']})" for movie in movies]
        selected_movies = st.multiselect(
            "Choose movies you like:",
            movie_titles,
            help="Select at least one movie to get recommendations"
        )
        
        # Number of recommendations slider
        n_recommendations = st.slider(
            "Number of recommendations:",
            min_value=5,
            max_value=20,
            value=10
        )
        
        # Extract movie IDs from selection
        if selected_movies:
            selected_movie_ids = [
                int(movie.split("(ID: ")[1].split(")")[0]) 
                for movie in selected_movies
            ]
            
            st.write(f"Selected {len(selected_movie_ids)} movies")
            
            # Get recommendations button
            if st.button("Get Recommendations", type="primary"):
                with st.spinner("Getting your recommendations..."):
                    recommendations = get_recommendations(
                        selected_movie_ids, 
                        n_recommendations
                    )
                    
                    if recommendations:
                        st.session_state['recommendations'] = recommendations
                        st.success(f"Found {len(recommendations)} recommendations!")
    
    with col2:
        st.subheader("Your Recommendations")
        
        if 'recommendations' in st.session_state:
            recommendations = st.session_state['recommendations']
            
            # Display recommendations
            for i, rec in enumerate(recommendations, 1):
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.write(f"**{i}. {rec['title']}**")
                        st.write(f"Movie ID: {rec['movie_id']}")
                    
                    with col_b:
                        # Display similarity score as a progress bar
                        similarity_pct = rec['similarity_score'] * 100
                        st.metric(
                            "Similarity", 
                            f"{similarity_pct:.1f}%"
                        )
                    
                    st.divider()
            
            # Create a chart of similarity scores
            if recommendations:
                chart_data = pd.DataFrame(recommendations)
                chart_data['similarity_percentage'] = chart_data['similarity_score'] * 100
                
                fig = px.bar(
                    chart_data.head(10),
                    x='similarity_percentage',
                    y='title',
                    orientation='h',
                    title='Top 10 Recommendations by Similarity Score',
                    labels={'similarity_percentage': 'Similarity %', 'title': 'Movie'}
                )
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("Select your favorite movies and click 'Get Recommendations' to see suggestions!")
    
    # Sidebar with statistics
    with st.sidebar:
        st.subheader("Dataset Statistics")
        st.metric("Total Movies", len(movies))
        
        if 'recommendations' in st.session_state:
            avg_similarity = sum(rec['similarity_score'] for rec in st.session_state['recommendations']) / len(st.session_state['recommendations'])
            st.metric("Average Similarity", f"{avg_similarity:.3f}")

if __name__ == "__main__":
    main()