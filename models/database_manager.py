from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """Interface for data managers in the MoviWeb application."""

    @abstractmethod
    def get_all_users(self):
        """Get all users from the data source.

        Returns:
            list: A list of user objects.
        """
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        """Get a specific user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            object: The user object if found, None otherwise.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Get all movies for a specific user.

        Args:
            user_id: The ID of the user whose movies to retrieve.

        Returns:
            list: A list of movie objects belonging to the user.
        """
        pass

    @abstractmethod
    def get_movie_by_id(self, movie_id):
        """Get a specific movie by its ID.

        Args:
            movie_id: The ID of the movie to retrieve.

        Returns:
            object: The movie object if found, None otherwise.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Delete a movie by its ID.

        Args:
            movie_id: The ID of the movie to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        pass