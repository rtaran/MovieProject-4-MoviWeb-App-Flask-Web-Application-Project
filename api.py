# api.py
from flask import Blueprint, jsonify, request, current_app
from flask.views import MethodView
from datamanager.sqlite_data_manager import SQLiteDataManager

api_bp = Blueprint('api', __name__)
data_manager = None


@api_bp.record
def record_params(setup_state):
    """
    This function runs when the blueprint is registered
    and gives us access to the app object
    """
    global data_manager
    app = setup_state.app
    data_manager = app.config.get('data_manager')


class UsersAPI(MethodView):
    def get(self, user_id=None):
        """Get all users or a specific user by ID"""
        if user_id is None:
            users = data_manager.get_all_users()
            return jsonify({
                'status': 'success',
                'data': [{'id': user.id, 'username': user.username} for user in users]
            })
        else:
            user = data_manager.User.query.get(user_id)
            if not user:
                return jsonify({'status': 'error', 'message': 'User not found'}), 404
            return jsonify({
                'status': 'success',
                'data': {'id': user.id, 'username': user.username}
            })

    def post(self):
        """Create a new user"""
        if not request.is_json:
            return jsonify({'status': 'error', 'message': 'Invalid content type, expected JSON'}), 400

        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({'status': 'error', 'message': 'Username is required'}), 400

        try:
            user = data_manager.add_user(username)
            return jsonify({
                'status': 'success',
                'message': 'User created successfully',
                'data': {'id': user.id, 'username': user.username}
            }), 201
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


class MoviesAPI(MethodView):
    def get(self, user_id, movie_id=None):
        """Get all movies for a user or a specific movie by ID"""
        # Check if user exists
        user = data_manager.User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

        if movie_id is None:
            # Get all movies for user
            movies = data_manager.get_user_movies(user_id)
            return jsonify({
                'status': 'success',
                'data': [{
                    'id': movie.id,
                    'name': movie.name,
                    'director': movie.director,
                    'year': movie.year,
                    'rating': movie.rating
                } for movie in movies]
            })
        else:
            # Get specific movie
            movie = data_manager.Movie.query.get(movie_id)
            if not movie or movie.user_id != user_id:
                return jsonify({'status': 'error', 'message': 'Movie not found for this user'}), 404

            return jsonify({
                'status': 'success',
                'data': {
                    'id': movie.id,
                    'name': movie.name,
                    'director': movie.director,
                    'year': movie.year,
                    'rating': movie.rating
                }
            })

    def post(self, user_id):
        """Add a new movie for a user"""
        # Check if user exists
        user = data_manager.User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

        if not request.is_json:
            return jsonify({'status': 'error', 'message': 'Invalid content type, expected JSON'}), 400

        data = request.get_json()
        name = data.get('name')
        director = data.get('director')
        year = data.get('year')
        rating = data.get('rating')

        if not name:
            return jsonify({'status': 'error', 'message': 'Movie name is required'}), 400

        try:
            movie = data_manager.add_movie(user_id, name, director, year, rating)
            return jsonify({
                'status': 'success',
                'message': 'Movie added successfully',
                'data': {
                    'id': movie.id,
                    'name': movie.name,
                    'director': movie.director,
                    'year': movie.year,
                    'rating': movie.rating
                }
            }), 201
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    def put(self, user_id, movie_id):
        """Update a movie"""
        # Check if movie exists and belongs to user
        movie = data_manager.Movie.query.get(movie_id)
        if not movie or movie.user_id != user_id:
            return jsonify({'status': 'error', 'message': 'Movie not found for this user'}), 404

        if not request.is_json:
            return jsonify({'status': 'error', 'message': 'Invalid content type, expected JSON'}), 400

        data = request.get_json()
        name = data.get('name', movie.name)
        director = data.get('director', movie.director)
        year = data.get('year', movie.year)
        rating = data.get('rating', movie.rating)

        try:
            updated_movie = data_manager.update_movie(movie_id, name, director, year, rating)
            return jsonify({
                'status': 'success',
                'message': 'Movie updated successfully',
                'data': {
                    'id': updated_movie.id,
                    'name': updated_movie.name,
                    'director': updated_movie.director,
                    'year': updated_movie.year,
                    'rating': updated_movie.rating
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    def delete(self, user_id, movie_id):
        """Delete a movie"""
        # Check if movie exists and belongs to user
        movie = data_manager.Movie.query.get(movie_id)
        if not movie or movie.user_id != user_id:
            return jsonify({'status': 'error', 'message': 'Movie not found for this user'}), 404

        try:
            result = data_manager.delete_movie(movie_id)
            if result:
                return jsonify({
                    'status': 'success',
                    'message': 'Movie deleted successfully'
                })
            else:
                return jsonify({'status': 'error', 'message': 'Failed to delete movie'}), 500
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


class ReviewsAPI(MethodView):
    def get(self, movie_id=None, review_id=None):
        """Get reviews for a movie or a specific review"""
        if review_id is not None:
            # Get specific review
            review = data_manager.get_review(review_id)
            if not review:
                return jsonify({'status': 'error', 'message': 'Review not found'}), 404

            return jsonify({
                'status': 'success',
                'data': {
                    'id': review.id,
                    'user_id': review.user_id,
                    'movie_id': review.movie_id,
                    'text': review.text,
                    'rating': review.rating,
                    'created_at': review.created_at,
                    'updated_at': review.updated_at
                }
            })
        elif movie_id is not None:
            # Get all reviews for a movie
            movie = data_manager.Movie.query.get(movie_id)
            if not movie:
                return jsonify({'status': 'error', 'message': 'Movie not found'}), 404

            reviews = data_manager.get_movie_reviews(movie_id)
            return jsonify({
                'status': 'success',
                'data': [{
                    'id': review.id,
                    'user_id': review.user_id,
                    'username': review.author.username,
                    'movie_id': review.movie_id,
                    'text': review.text,
                    'rating': review.rating,
                    'created_at': str(review.created_at),
                    'updated_at': str(review.updated_at)
                } for review in reviews]
            })
        else:
            return jsonify({'status': 'error', 'message': 'Missing movie_id parameter'}), 400

    def post(self, movie_id):
        """Add a new review for a movie"""
        # Check if movie exists
        movie = data_manager.Movie.query.get(movie_id)
        if not movie:
            return jsonify({'status': 'error', 'message': 'Movie not found'}), 404

        if not request.is_json:
            return jsonify({'status': 'error', 'message': 'Invalid content type, expected JSON'}), 400

        data = request.get_json()
        user_id = data.get('user_id')
        text = data.get('text')
        rating = data.get('rating')

        if not user_id or not text or rating is None:
            return jsonify({'status': 'error', 'message': 'Missing required fields: user_id, text, rating'}), 400

        # Check if user exists
        user = data_manager.User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

        try:
            review = data_manager.add_review(user_id, movie_id, text, rating)
            return jsonify({
                'status': 'success',
                'message': 'Review added successfully',
                'data': {
                    'id': review.id,
                    'user_id': review.user_id,
                    'movie_id': review.movie_id,
                    'text': review.text,
                    'rating': review.rating,
                    'created_at': str(review.created_at),
                    'updated_at': str(review.updated_at)
                }
            }), 201
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    def put(self, review_id):
        """Update a review"""
        review = data_manager.get_review(review_id)
        if not review:
            return jsonify({'status': 'error', 'message': 'Review not found'}), 404

        if not request.is_json:
            return jsonify({'status': 'error', 'message': 'Invalid content type, expected JSON'}), 400

        data = request.get_json()
        text = data.get('text', review.text)
        rating = data.get('rating', review.rating)

        try:
            updated_review = data_manager.update_review(review_id, text, rating)
            return jsonify({
                'status': 'success',
                'message': 'Review updated successfully',
                'data': {
                    'id': updated_review.id,
                    'user_id': updated_review.user_id,
                    'movie_id': updated_review.movie_id,
                    'text': updated_review.text,
                    'rating': updated_review.rating,
                    'created_at': str(updated_review.created_at),
                    'updated_at': str(updated_review.updated_at)
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    def delete(self, review_id):
        """Delete a review"""
        review = data_manager.get_review(review_id)
        if not review:
            return jsonify({'status': 'error', 'message': 'Review not found'}), 404

        try:
            result = data_manager.delete_review(review_id)
            if result:
                return jsonify({
                    'status': 'success',
                    'message': 'Review deleted successfully'
                })
            else:
                return jsonify({'status': 'error', 'message': 'Failed to delete review'}), 500
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


# Register the Users API endpoints
users_view = UsersAPI.as_view('users_api')
api_bp.add_url_rule('/users', view_func=users_view, methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>', view_func=users_view, methods=['GET'])

# Register the Movies API endpoints
movies_view = MoviesAPI.as_view('movies_api')
api_bp.add_url_rule('/users/<int:user_id>/movies', view_func=movies_view, methods=['GET', 'POST'])
api_bp.add_url_rule('/users/<int:user_id>/movies/<int:movie_id>', view_func=movies_view,
                    methods=['GET', 'PUT', 'DELETE'])

# Register the Reviews API endpoints
reviews_view = ReviewsAPI.as_view('reviews_api')
api_bp.add_url_rule('/movies/<int:movie_id>/reviews', view_func=reviews_view, methods=['GET', 'POST'])
api_bp.add_url_rule('/reviews/<int:review_id>', view_func=reviews_view, methods=['GET', 'PUT', 'DELETE'])