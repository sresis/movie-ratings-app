"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
	"""view the homepage."""
	
	return render_template('homepage.html')

@app.route('/movies')
def view_movies():
	"""view the movies."""

	movies = crud.return_all_movies()
	return render_template('all_movies.html', movies=movies)


@app.route('/movies/<movie_id>')
def show_movie_details(movie_id):
	"""show movie details on page."""

	movie = crud.get_movie_by_id(movie_id)
	
	return render_template('movie_details.html', movie=movie)

@app.route('/users')
def view_users():
	"""view the movies."""

	users = crud.return_all_users()
	return render_template('all_users.html', users=users)

@app.route('/users', methods=['POST'])
def create_user():
	"""Create a new user."""
	# if user already exists, return user
	email = request.form['email']
	password = request.form['password']

	user = crud.get_user_by_email(email)
	if user:
		flash('Sorry that email is already registered')
	else:
		crud.create_user(email, password)
		flash('Your account was created! Please log in.')


	return redirect('/')


@app.route('/login', methods=['POST'])
def login_user():
	## right now it only lets you log in with existing
	#session['show_login'] == True
	# gets email and password from form
	email = request.form['email']
	password = request.form['password']
	# gets user info based on email
	user = crud.get_user_by_email(email)
	session['user'] = []
	# checks if pasword in db matches form pasword
	if user.password == password:
		#adds user to session
		session['user'] = user.user_id
		flash('you are logged in!')
		return redirect('/')

	else:
		flash('incorrect login.')
		return redirect('/')




@app.route('/users/<user_id>')
def show_user_details(user_id):
	"""show movie details on page."""

	user = crud.get_user_by_id(user_id)
	
	return render_template('user_details.html', user=user)






if __name__ == '__main__':
	connect_to_db(app)
	app.run(host='0.0.0.0', debug=True)
