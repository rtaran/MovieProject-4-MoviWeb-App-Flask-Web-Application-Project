import sqlite3
import os
from .data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):
    """SQLite implementation of the DataManager interface."""

    def __init__(self, db_path='data/movieweb.db'):
        """Initialize the SQLite database manager.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.connection = None
        self.create_tables()

    def connect(self):
        """Create a connection to the SQLite database.

        Returns:
            sqlite3.Connection: A connection to the database.
        """
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_tables(self):
        """Create the necessary tables if they don't exist."""
        conn = self.connect()
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        ''')

        # Create movies table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            director TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        # Insert some sample users if the table is empty
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            sample_users = ['Alice', 'Bob', 'Charlie', 'Diana']
            cursor.executemany(
                'INSERT INTO users (name) VALUES (?)',
                [(user,) for user in sample_users]
            )

            # Add some sample movies for testing
            cursor.execute('SELECT id FROM users WHERE name = ?', ('Alice',))
            alice_id = cursor.fetchone()[0]

            sample_movies = [
                (alice_id, 'The Shawshank Redemption', 'Frank Darabont', 1994, 9.3),
                (alice_id, 'The Godfather', 'Francis Ford Coppola', 1972, 9.2),
                (alice_id, 'Inception', 'Christopher Nolan', 2010, 8.8)
            ]

            cursor.executemany(
                'INSERT INTO movies (user_id, name, director, year, rating) VALUES (?, ?, ?, ?, ?)',
                sample_movies
            )

        conn.commit()
        self.close()

    def get_all_users(self):
        """Get all users from the database.

        Returns:
            list: A list of user dictionaries.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY name')
        users = [dict(user) for user in cursor.fetchall()]
        self.close()
        return users

    def get_user_by_id(self, user_id):
        """Get a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            dict: The user dictionary if found, None otherwise.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        self.close()

        if user:
            return dict(user)
        return None

    def get_user_movies(self, user_id):
        """Get all movies for a specific user.

        Args:
            user_id: The ID of the user whose movies to retrieve.

        Returns:
            list: A list of movie dictionaries belonging to the user.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM movies 
        WHERE user_id = ? 
        ORDER BY name
        ''', (user_id,))
        movies = [dict(movie) for movie in cursor.fetchall()]
        self.close()
        return movies

    def get_movie_by_id(self, movie_id):
        """Get a movie by its ID.

        Args:
            movie_id: The ID of the movie to retrieve.

        Returns:
            dict: The movie dictionary if found, None otherwise.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
        movie = cursor.fetchone()
        self.close()

        if movie:
            return dict(movie)
        return None

    def add_movie(self, user_id, name, director, year, rating):
        """Add a new movie for a user.

        Args:
            user_id: The ID of the user to add the movie for.
            name: The name/title of the movie.
            director: The director of the movie.
            year: The release year of the movie.
            rating: The rating of the movie.

        Returns:
            int: The ID of the newly added movie.
        """
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute('''
            INSERT INTO movies (user_id, name, director, year, rating)
            VALUES (?, ?, ?, ?, ?)
            ''', (user_id, name, director, year, rating))
            conn.commit()
            movie_id = cursor.lastrowid
            return movie_id
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return None
        finally:
            self.close()

    def update_movie(self, movie_id, name, director, year, rating):
        """Update an existing movie.

        Args:
            movie_id: The ID of the movie to update.
            name: The new name/title of the movie.
            director: The new director of the movie.
            year: The new release year of the movie.
            rating: The new rating of the movie.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute('''
            UPDATE movies
            SET name = ?, director = ?, year = ?, rating = ?
            WHERE id = ?
            ''', (name, director, year, rating, movie_id))
            conn.commit()
            success = cursor.rowcount > 0
            return success
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            self.close()

    def delete_movie(self, movie_id):
        """Delete a movie by its ID.

        Args:
            movie_id: The ID of the movie to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
            conn.commit()
            success = cursor.rowcount > 0
            return success
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            self.close()