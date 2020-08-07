"""Script to seed the database"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()


with open('data/movies.json') as f:
	movie_data = json.loads(f.read())

# adds movies to database
movies_in_db = []
for movie in movie_data:
	title, overview, poster_path = (movie['title'], movie['overview'],
					 movie['poster_path'])
	release_date = datetime.strptime(movie['release_date'], "%Y-%m-%d")

	db_movie = crud.create_movie(title, overview, release_date, poster_path)

	movies_in_db.append(db_movie);

#creates 10 random users

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    new_user = crud.create_user(email, password)

    # creates 10 ratings for each user
    for n in range(10):
    	user_rating = randint(1, 5)
    	user_movie = choice(movies_in_db)

    	crud.create_rating(new_user, user_movie, user_rating)


