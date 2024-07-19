import streamlit as st
import requests

API_KEY = "8263fee1adffb0f015403aa42baf877c"
BASE_URL = "https://api.themoviedb.org/3"
LANGUAGE_CODE = "en-US"

def make_api_request(url):
    try:
        response = requests.get(url, timeout=20.0)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def search_movie_id(movie_title):
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={movie_title}&language={LANGUAGE_CODE}"
    data = make_api_request(url)
    if data and 'results' in data and data['results']:
        return data['results'][0]['id']
    return None

def get_movie_recommendations(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/recommendations?api_key={API_KEY}&language={LANGUAGE_CODE}"
    data = make_api_request(url)
    return data['results'][:16] if data and 'results' in data else []

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language={LANGUAGE_CODE}"
    return make_api_request(url)

def get_popular_movies(region):
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&region={region}"
    data = make_api_request(url)
    return data['results'][:16] if data and 'results' in data else []

st.title('Movie Recommendation App')

def display_movie_grid(movies):
    for i in range(0, len(movies), 4):
        cols = st.columns(4)
        for col, movie in zip(cols, movies[i:i+4]):
            with col:
                if 'poster_path' in movie and movie['poster_path']:
                    poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    st.image(poster_url, use_column_width=True)
                st.write(movie['title'])

def main():
    st.header("Movie Recommendations")
    movie_title = st.text_input('Enter a movie title')
    
    if st.button('Get Recommendations'):
        with st.spinner('Searching for the movie...'):
            movie_id = search_movie_id(movie_title)
        
        if movie_id:
            with st.spinner('Getting recommendations...'):
                recommendations = get_movie_recommendations(movie_id)
            
            if recommendations:
                st.subheader('Recommended Movies:')
                display_movie_grid(recommendations)
            else:
                st.warning("Unable to get recommendations.")
        else:
            st.warning("Movie not found. Please check the title and try again.")

    st.header("Popular Movies Right Now")
    st.subheader("Hollywood")
    popular_hollywood = get_popular_movies('US')
    if popular_hollywood:
        display_movie_grid(popular_hollywood)
    else:
        st.warning("Unable to fetch popular movies from Hollywood.")
if __name__ == "__main__":
    main()