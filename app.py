import streamlit as st
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, 'u.data')
item_path = os.path.join(current_dir, 'u.item')

st.set_page_config(page_title="Movie Dashboard", layout="wide")

st.title("🎬 Movie Analytics Dashboard")
st.markdown("Analyze user behavior and movie trends")
st.sidebar.title("Controls")

min_ratings = st.sidebar.slider("Minimum number of ratings", 0, 500, 100)




ratings = pd.read_csv('data_path', sep='\t', 
                      names=['userId', 'movieId', 'rating', 'timestamp'])

movies = pd.read_csv('item_path', sep='|', encoding='latin-1', header=None)
movies = movies[[0, 1]]
movies.columns = ['movieId', 'title']

data = pd.merge(ratings, movies, on='movieId')


st.subheader("Platform Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Ratings", len(data))
col2.metric("Total Users", data['userId'].nunique())
col3.metric("Total Movies", data['movieId'].nunique())


if st.checkbox("Show raw data"):
    st.write(data.head())

col1, col2 = st.columns(2)

with col1:
    st.subheader("Most Watched Movies")
    top_movies = data['title'].value_counts().head(10)
    st.bar_chart(top_movies.sort_values())

with col2:
    st.subheader("Rating Distribution")
    st.bar_chart(data['rating'].value_counts().sort_index())



st.subheader("Highest Rated Movies")

movie_ratings = data.groupby('title')['rating'].mean()
movie_counts = data['title'].value_counts()

movie_summary = pd.DataFrame({
    'avg_rating': movie_ratings,
    'num_ratings': movie_counts
})

top_rated = movie_summary[movie_summary['num_ratings'] > min_ratings] \
    .sort_values(by='avg_rating', ascending=False).head(10)

st.dataframe(top_rated)

st.subheader("Search Movie")

movie_name = st.text_input("Enter movie name")

if movie_name:
    result = data[data['title'].str.contains(movie_name, case=False)]
    st.write(f"Found {len(result)} results")
    st.write(result.head(10))

st.subheader("Insights")

st.write("""
- Most users interact with a small number of movies.
- Popular movies are those that drive engagement.
- Highly rated movies are key for recommendations.
""")

st.subheader("What I Learned")

st.write("""
While working on this project, I noticed that most users are not very active,
and only a small group contributes a large portion of the ratings.

This shows how important it is for platforms to focus on engagement
and personalized recommendations.
""")


