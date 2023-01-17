import numpy as np
import pandas as pd

links_df = pd.read_csv('data/links.csv')
movies_df = pd.read_csv('data/movies.csv')
ratings_df = pd.read_csv('data/ratings.csv')
tags_df = pd.read_csv('data/tags.csv')

df = movies_df.merge(ratings_df, on='movieId')

M_j = 'John Wick (2014)' # Title as input, now it's just one movie
recommended_movies = []

# Find the movie in the database, and sort it by rating
movie_db = df[df['title'] == M_j]\
            .sort_values(by='rating', ascending=False)

# Get the first 5 users who liked this movie
for user in movie_db.iloc[:5]['userId'].values:
    
    # Get the rated movies for this user
    rated_movies = df[df['userId'] == user]
    
    # Get the five biggest rated movie by this user
    rated_movies = rated_movies[rated_movies['title'] != M_j]\
                    .sort_values(by='rating', ascending=False)\
                    .iloc[:5]
    
    # Add these to the recommendations
    recommended_movies.extend(list(rated_movies['title'].values))
    
recommended_movies = np.unique(recommended_movies)


gmovie_genres = df[df['title'] == M_j].iloc[0]['genres'].split('|')
scores = {}  # {title: score ...}

for movie in recommended_movies:
    movied = df[df['title'] == movie].iloc[0]
    movie_genres = movied['genres'].split('|')
    score = 0
    
    # How many gmovie_genre can be found in movie_genres?
    for gmovie_genre in gmovie_genres:
        if gmovie_genre in movie_genres:
            score += 1
    
    scores[movie] = score
    
# Sort them on score and reverse it, because the bigger the score the better 
recommended_movies = sorted(scores, key=lambda x: scores[x])[::-1]  

for movie in recommended_movies:
    print(movie)
