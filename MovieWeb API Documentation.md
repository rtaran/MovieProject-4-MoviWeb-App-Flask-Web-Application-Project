# MovieWeb API Documentation

This document describes the RESTful API endpoints available for the MovieWeb application.

## Base URL

All API endpoints are prefixed with `/api`.

## Response Format

All API responses are in JSON format and follow this structure:

```json
{
  "status": "success" or "error",
  "message": "Optional message explaining the result",
  "data": "Response data (varies by endpoint)"
}
```

## Authentication

Currently, the API does not require authentication.

## Endpoints

### Users

#### GET /api/users
- **Description**: Retrieve a list of all users
- **Parameters**: None
- **Response**: List of users with their IDs and usernames

#### GET /api/users/{user_id}
- **Description**: Retrieve details for a specific user
- **Parameters**: `user_id` - ID of the user to retrieve
- **Response**: User object with ID and username

#### POST /api/users
- **Description**: Create a new user
- **Parameters**: JSON body containing:
  - `username` (required): Username for the new user
- **Response**: The created user object

### Movies

#### GET /api/users/{user_id}/movies
- **Description**: Retrieve all movies for a specific user
- **Parameters**: `user_id` - ID of the user whose movies to retrieve
- **Response**: List of movie objects

#### GET /api/users/{user_id}/movies/{movie_id}
- **Description**: Retrieve a specific movie for a user
- **Parameters**:
  - `user_id` - ID of the user
  - `movie_id` - ID of the movie to retrieve
- **Response**: Movie object with details

#### POST /api/users/{user_id}/movies
- **Description**: Add a new movie for a user
- **Parameters**:
  - `user_id` - ID of the user
  - JSON body containing:
    - `name` (required): Movie name
    - `director`: Movie director
    - `year`: Release year
    - `rating`: Movie rating
- **Response**: The created movie object

#### PUT /api/users/{user_id}/movies/{movie_id}
- **Description**: Update a movie
- **Parameters**:
  - `user_id` - ID of the user
  - `movie_id` - ID of the movie to update
  - JSON body containing fields to update (name, director, year, rating)
- **Response**: The updated movie object

#### DELETE /api/users/{user_id}/movies/{movie_id}
- **Description**: Delete a movie
- **Parameters**:
  - `user_id` - ID of the user
  - `movie_id` - ID of the movie to delete
- **Response**: Success/error message

### Reviews

#### GET /api/movies/{movie_id}/reviews
- **Description**: Get all reviews for a specific movie
- **Parameters**: `movie_id` - ID of the movie
- **Response**: List of review objects

#### GET /api/reviews/{review_id}
- **Description**: Get a specific review
- **Parameters**: `review_id` - ID of the review
- **Response**: Review object with details

#### POST /api/movies/{movie_id}/reviews
- **Description**: Add a new review for a movie
- **Parameters**:
  - `movie_id` - ID of the movie
  - JSON body containing:
    - `user_id` (required): ID of the user writing the review
    - `text` (required): Review text
    - `rating` (required): Rating value
- **Response**: The created review object

#### PUT /api/reviews/{review_id}
- **Description**: Update a review
- **Parameters**:
  - `review_id` - ID of the review to update
  - JSON body containing fields to update (text, rating)
- **Response**: The updated review object

#### DELETE /api/reviews/{review_id}
- **Description**: Delete a review
- **Parameters**: `review_id` - ID of the review to delete
- **Response**: Success/error message

## Example Usage

### List all users

```bash
curl -X GET http://localhost:5000/api/users
```

### Add a new movie for a user

```bash
curl -X POST http://localhost:5000/api/users/1/movies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "The Matrix",
    "director": "The Wachowskis",
    "year": 1999,
    "rating": 8.7
  }'
```

### Add a review for a movie

```bash
curl -X POST http://localhost:5000/api/movies/1/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "text": "This is a great movie!",
    "rating": 9.0
  }'
```