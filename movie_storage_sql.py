"""
SQLite-backed storage helpers for the Movie app.

Creates the movies table on import if it does not exist and exposes CRUD
functions to list, add, delete and update movies.
"""

from sqlalchemy import create_engine, text
from ombd_client import fetch_movie_data

# Database connection URL (relative SQLite file in the project root)
DB_URL = "sqlite:///movies.db"

# Create the engine (echo=True logs SQL statements for debugging)
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_image_url STRING NOT NULL   
        )               
    """))
    connection.commit()


def list_movies():
    """
    Retrieve all movies from the database.
    :return: Mapping of title to a dict with keys "year", "rating", and "poster_image_url".
    """
    with engine.connect() as connection:
        result = connection.execute(
            text(
                """SELECT title, year, rating , poster_image_url 
                FROM movies"""
            )
        )
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster_image_url": row[3]} for row in movies}


def add_movie(title, year, rating, poster_image_url):
    """
    Add a new movie to the database.
    Fetches metadata from OMDb (demonstration call) and inserts the
    provided fields into the local SQLite database.
    """
    movie_data = fetch_movie_data(title)

    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """INSERT INTO movies (title, year, rating, poster_image_url)     
                    VALUES (:title, :year, :rating, :poster_image_url)"""
                ),
                    {"title": title, "year": year, "rating": rating, "poster_image_url": poster_image_url}
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """
    Delete a movie from the database by its title.
    :param title: The movie title to remove.
    :return: None
    """
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """DELETE FROM movies 
                    WHERE title = :title"""
                ),
                    {"title": title}
            )
            connection.commit()
            print(f"Movie '{title}' was successfully deleted")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """
    Update a movie's rating in the database.
    :param title: Movie title (case-insensitive comparison).
    :param rating: New rating value to set.
    :return: None
    """
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    """UPDATE movies 
                    SET rating = :rating 
                    WHERE LOWER (title) = :title"""
                ),
                    {"title": title.lower(), "rating": rating}
            )
            connection.commit()
            print(f"Movie '{title}' was successfully updated")
        except Exception as e:
            print(f"Error: {e}")
