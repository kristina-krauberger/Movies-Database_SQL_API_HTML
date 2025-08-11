"""
This module contains tests for the SQL storage functions for movies.
It exercises the add_movie, list_movies, update_movie, and delete_movie
functions to ensure proper CRUD operations on the movie database.
"""
from movie_storage_sql import add_movie, list_movies, delete_movie, update_movie


def test_add_movie():
    """Test adding a movie"""
    add_movie("Inception", 2010, 8.8, "N/A")


def test_list_movie():
    """Test listing movies"""
    movies = list_movies()
    print(movies)


def test_update_movie():
    """Test updating a movie's rating"""
    update_movie("Inception", 9.0)
    print(list_movies())


def test_delete_movie():
    """Test deleting a movie"""
    delete_movie("Inception")
    print(list_movies())  # Should be empty if it was the only movie


# Run the tests in order
test_add_movie()
test_list_movie()
test_update_movie()
test_delete_movie()