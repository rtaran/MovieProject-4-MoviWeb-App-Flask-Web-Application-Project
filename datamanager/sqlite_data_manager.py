from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface
from datetime import datetime
from models import db, User, Movie, Review

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = db
        self.app = app
        self.db.init_app(app)

        # Save model classes as attributes
        self.User = User
        self.Movie = Movie
        self.Review = Review

        # Create tables
        with app.app_context():
            self.db.create_all()

    def get_all_users(self):
        return self.User.query.all()

    def get_user_by_id(self, user_id):
        return self.User.query.get(user_id)

    def get_user_movies(self, user_id):
        # Get all reviews for the user
        reviews = self.Review.query.filter_by(user_id=user_id).all()
        # Extract the movie_ids from the reviews
        movie_ids = [review.movie_id for review in reviews]
        # Get all movies with these ids
        return self.Movie.query.filter(self.Movie.id.in_(movie_ids)).all()

    def add_user(self, username):
        user = self.User(username=username)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def add_movie(self, user_id, name, director, year, rating):
        # Create the movie
        movie = self.Movie(title=name)
        self.db.session.add(movie)
        self.db.session.commit()

        # Create a review to connect the user and movie
        review = self.Review(user_id=user_id, movie_id=movie.id, rating=rating or 0, comment="")
        self.db.session.add(review)
        self.db.session.commit()

        return movie

    def update_movie(self, movie_id, name, director, year, rating):
        movie = self.Movie.query.get(movie_id)
        if movie:
            movie.title = name
            self.db.session.commit()
            return movie
        return None

    def delete_movie(self, movie_id):
        movie = self.Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
            return True
        return False

    # Review-related methods
    def get_movie_reviews(self, movie_id):
        return self.Review.query.filter_by(movie_id=movie_id).all()

    def get_user_reviews(self, user_id):
        return self.Review.query.filter_by(user_id=user_id).all()

    def add_review(self, user_id, movie_id, text, rating):
        review = self.Review(user_id=user_id, movie_id=movie_id, comment=text, rating=rating)
        self.db.session.add(review)
        self.db.session.commit()
        return review

    def update_review(self, review_id, text, rating):
        review = self.Review.query.get(review_id)
        if review:
            review.comment = text
            review.rating = rating
            self.db.session.commit()
            return review
        return None

    def delete_review(self, review_id):
        review = self.Review.query.get(review_id)
        if review:
            self.db.session.delete(review)
            self.db.session.commit()
            return True
        return False

    def get_review(self, review_id):
        return self.Review.query.get(review_id)
