import streamlit as st
import pickle
import pandas as pd
import requests
import gzip

# Load movies and similarity matrix
movies = pickle.load(open("movies2.pkl", "rb"))
# Open the gzip file and load the pickle data
with gzip.open("similarity2.pkl.gz", "rb") as f:
    similarity = pickle.load(f)



# Create a crosstab of movies and genres (assuming this is used elsewhere)
movie_cross_table = pd.crosstab(movies['title'], movies['genres'])

# Wrap the similarity array in a pandas DataFrame
cosine_similarity_df = pd.DataFrame(similarity, index=movie_cross_table.index, columns=movie_cross_table.index)

# List of movie titles
movies_list = movies['title'].values

st.header("Movies Recommender System")

# Selectbox for movie selection
selected_movie = st.selectbox("Select movie:", movies_list)


# Function to recommend movies
def recommend(movie):
    # Get the index of the selected movie
    index = movies[movies['title'] == movie].index[0]
    # Get a list of similar movies in descending order of similarity
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
   # recommend_poster = []
    # Get the titles and posters of the top 5 recommended movies
    for i in distances[1:6]:
       #movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
    #    recommend_poster.append(fetch_poster(movie_id))
    return recommended_movies #, recommend_poster


# Button to show recommendations
if st.button("Show Recommend"):
    recommendations=recommend(selected_movie) #, movie_posters = recommend(selected_movie)
    st.write(f"Here are the top 5 movie recommendations similar to '{selected_movie}':")

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommendations[i])
            #st.image(movie_posters[i])


