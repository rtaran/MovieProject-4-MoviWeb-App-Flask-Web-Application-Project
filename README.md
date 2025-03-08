# MovieWeb App

A Flask-based web application for managing movie collections for multiple users. The app allows users to add, update, and delete movies from their personal collections, with movie data automatically fetched from the OMDb API.

## Features

- User management: Create and view users
- Movie collection management: Add, update, and delete movies for each user
- OMDb API integration: Automatically fetch movie details when adding a film
- SQLite database storage: Lightweight and portable database solution

## Project Structure

```
moviewebapp/
├── app.py                         # Main Flask application
├── movieweb.db                    # SQLite database (created at runtime)
├── datamanager/
│   ├── __init__.py                # Package initialization file
│   ├── data_manager_interface.py  # Abstract interface for data managers
│   └── sqlite_data_manager.py     # SQLite implementation of data manager
├── templates/
│   ├── 404.html                   # 404 error page
│   ├── 500.html                   # 500 error page
│   ├── add_movie.html             # Form for adding movies
│   ├── add_user.html              # Form for adding users
│   ├── home.html                  # Home page
│   ├── update_movie.html          # Form for updating movies
│   ├── user_movies.html           # Page showing a user's movies
│   └── users.html                 # List of all users
```

## Prerequisites

- Python 3.6+
- Flask
- Flask-SQLAlchemy
- Requests

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/moviewebapp.git
   cd moviewebapp
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install flask flask-sqlalchemy requests
   ```

4. Set up the OMDb API key (current key: 5429604c)
   - If you prefer to use your own API key, you can get one at [omdbapi.com](http://www.omdbapi.com/)
   - Replace the API key in `app.py`

## Running the Application

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage

1. **Adding a User**:
   - Navigate to the home page
   - Click on "Add User"
   - Enter a username
   - Click "Add User"

2. **Adding a Movie**:
   - Click on a user's name
   - Click "Add Movie"
   - Enter the movie name
   - Click "Add Movie" (details will be fetched from OMDb)

3. **Updating a Movie**:
   - Navigate to a user's movie list
   - Click "Edit" next to the movie
   - Update information
   - Click "Update Movie"

4. **Deleting a Movie**:
   - Navigate to a user's movie list
   - Click "Delete" next to the movie

## Architecture

This application uses a clean architecture approach with a clear separation of concerns:

- **Data Layer**: The `DataManagerInterface` defines the contract for data operations, and `SQLiteDataManager` implements this interface for SQLite.
- **Application Layer**: The Flask application in `app.py` handles HTTP requests and responses.
- **Presentation Layer**: HTML templates in the `templates` folder render the user interface.


## License

[MIT License](LICENSE)