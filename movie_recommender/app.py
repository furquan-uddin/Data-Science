import pickle
import streamlit as st
import requests
import os

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"  # Your TMDB API Key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    except:
        pass

    return "https://via.placeholder.com/500x750.png?text=No+Image"  # Fallback image if no poster

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")  # Wide layout
st.header('🎬 Movie Recommender System')

# Load the movie dataset and similarity matrix
try:
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Use st.columns to display images in a row
    cols = st.columns(5)
    
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
