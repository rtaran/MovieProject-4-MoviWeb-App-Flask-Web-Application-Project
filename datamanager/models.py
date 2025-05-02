from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    reviews = db.relationship(
        'Review', backref='author', lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<User {self.username}>'

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    reviews = db.relationship(
        'Review', backref='movie', lazy=True,
        cascade="all, delete-orphan"
    )

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
#
# # Create global db instance to be initialized later
# db = SQLAlchemy()
#
# # Define models
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     # Add relationship to reviews
#     reviews = db.relationship(
#         'Review',
#         backref='author',
#         lazy=True,
#         cascade="all, delete-orphan"
#     )
#
#     def __repr__(self):
#         return f'<User {self.username}>'
#
#
# class Movie(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     name = db.Column(db.String(120), nullable=False)
#     director = db.Column(db.String(120))
#     year = db.Column(db.Integer)
#     rating = db.Column(db.Float)
#     # Add relationship to reviews
#     reviews = db.relationship(
#         'Review',
#         backref='movie',
#         lazy=True,
#         cascade="all, delete-orphan"
#     )
#
#     def __repr__(self):
#         return f'<Movie {self.name}>'
#
#
# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
#     text = db.Column(db.Text, nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#     def __repr__(self):
#         return f'<Review {self.id} by User {self.user_id} for Movie {self.movie_id}>'
