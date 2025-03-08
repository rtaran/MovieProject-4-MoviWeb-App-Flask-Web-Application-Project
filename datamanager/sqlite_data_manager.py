from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface
from datetime import datetime


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = SQLAlchemy(app)
        self.app = app

        # Define models within app context
        class User(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            username = self.db.Column(self.db.String(80), unique=True, nullable=False)
            # Add relationship to reviews
            reviews = self.db.relationship('Review', backref='author', lazy=True, cascade="all, delete-orphan")

            def __repr__(self):
                return f'<User {self.username}>'

        class Movie(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            user_id = self.db.Column(self.db.Integer, self.db.ForeignKey('user.id'), nullable=False)
            name = self.db.Column(self.db.String(120), nullable=False)
            director = self.db.Column(self.db.String(120))
            year = self.db.Column(self.db.Integer)
            rating = self.db.Column(self.db.Float)
            # Add relationship to reviews
            reviews = self.db.relationship('Review', backref='movie', lazy=True, cascade="all, delete-orphan")

            def __repr__(self):
                return f'<Movie {self.name}>'

        class Review(self.db.Model):
            id = self.db.Column(self.db.Integer, primary_key=True)
            user_id = self.db.Column(self.db.Integer, self.db.ForeignKey('user.id'), nullable=False)
            movie_id = self.db.Column(self.db.Integer, self.db.ForeignKey('movie.id'), nullable=False)
            text = self.db.Column(self.db.Text, nullable=False)
            rating = self.db.Column(self.db.Float, nullable=False)
            created_at = self.db.Column(self.db.DateTime, default=datetime.utcnow)
            updated_at = self.db.Column(self.db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

            def __repr__(self):
                return f'<Review {self.id} by User {self.user_id} for Movie {self.movie_id}>'

        # Save model classes as attributes
        self.User = User
        self.Movie = Movie
        self.Review = Review

        # Create tables
        with app.app_context():
            self.db.create_all()

    def get_all_users(self):
        return self.User.query.all()

    def get_user_movies(self, user_id):
        return self.Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, username):
        user = self.User(username=username)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def add_movie(self, user_id, name, director, year, rating):
        movie = self.Movie(user_id=user_id, name=name, director=director, year=year, rating=rating)
        self.db.session.add(movie)
        self.db.session.commit()
        return movie

    def update_movie(self, movie_id, name, director, year, rating):
        movie = self.Movie.query.get(movie_id)
        if movie:
            movie.name = name
            movie.director = director
            movie.year = year
            movie.rating = rating
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
        return self.Review.query.filter_by(movie_id=movie_id).order_by(self.Review.created_at.desc()).all()

    def get_user_reviews(self, user_id):
        return self.Review.query.filter_by(user_id=user_id).order_by(self.Review.created_at.desc()).all()

    def add_review(self, user_id, movie_id, text, rating):
        review = self.Review(user_id=user_id, movie_id=movie_id, text=text, rating=rating)
        self.db.session.add(review)
        self.db.session.commit()
        return review

    def update_review(self, review_id, text, rating):
        review = self.Review.query.get(review_id)
        if review:
            review.text = text
            review.rating = rating
            review.updated_at = datetime.utcnow()
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