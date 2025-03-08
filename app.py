from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movieweb.db'  # Fixed typo in DB name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)  # Secure secret key

# Initialize data manager after app configuration
data_manager = SQLiteDataManager(app)

OMDB_API_KEY = "5429604c"

def get_movie_data_from_omdb(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        if movie_data.get("Response") == "True":
            return movie_data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"OMDb API error: {e}")
        return None

@app.route('/')
def home():
    return redirect(url_for('list_users'))

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    user = data_manager.User.query.get_or_404(user_id)
    return render_template('user_movies.html', movies=movies, user=user)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        try:
            data_manager.add_user(username)
            flash('User added successfully!', 'success')
            return redirect(url_for('list_users'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
    return render_template('add_user.html')

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = data_manager.User.query.get_or_404(user_id)
    if request.method == 'POST':
        movie_name = request.form['name']
        movie_data = get_movie_data_from_omdb(movie_name)
        if movie_data:
            name = movie_data.get('Title')
            director = movie_data.get('Director')
            year = movie_data.get('Year')
            rating = movie_data.get('imdbRating')
            try:
                data_manager.add_movie(user_id, name, director, year, rating)
                flash('Movie added successfully!', 'success')
                return redirect(url_for('user_movies', user_id=user_id))
            except Exception as e:
                flash(f'An error occurred: {e}', 'error')
        else:
            flash('Movie not found on OMDb or API error.', 'error')
    return render_template('add_movie.html', user=user)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = data_manager.Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']
        try:
            data_manager.update_movie(movie_id, name, director, year, rating)
            flash('Movie updated successfully!', 'success')
            return redirect(url_for('user_movies', user_id=user_id))
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')
    return render_template('update_movie.html', movie=movie)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(movie_id)
        flash('Movie deleted successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
    return redirect(url_for('user_movies', user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)