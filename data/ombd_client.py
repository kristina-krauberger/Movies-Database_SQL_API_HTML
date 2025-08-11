"""
OMDb (omdbapi.com) client helpers.

Loads the API key from the environment variable `KEY` and exposes a
function to fetch movie metadata by title. Returns a 4-tuple
(year, rating, poster_image_url, title) or `None` if not found or on
HTTP/JSON error.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KEY")
API_URL = f"http://www.omdbapi.com/?apikey={API_KEY}&"


def fetch_movie_data(title):
    """
    Fetch movie metadata by title from OMDb.
    :param title: Movie title to look up.
    :return: A tuple (year, rating, poster_image_url, title) if found, otherwise None.
    """
    params = {"t": title}
    response = requests.get(API_URL, params=params)
    data = response.json()

    # API-Fehlerbehandlung: Film nicht gefunden
    if data.get("Response") == "False":
        print(f" Movie '{title}' not found: {data.get('Error')}")
        return None

    title = data["Title"]
    year = data["Year"]
    rating = data["imdbRating"]
    poster_image_url = data["Poster"]
    print(year, rating, poster_image_url, title)
    return year, rating, poster_image_url, title




