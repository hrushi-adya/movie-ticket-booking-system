import collections
from datetime import datetime, timezone
from decimal import Decimal


def generate_utc_timestamp():
    return datetime.now().isoformat()


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def decimal_to_native(obj):
    """Helper function to convert Decimal to int/float for JSON serialization."""
    if isinstance(obj, Decimal):
        # Convert to int if the Decimal represents a whole number, otherwise float
        return int(obj) if obj % 1 == 0 else float(obj)
    if isinstance(obj, list):
        return [decimal_to_native(i) for i in obj]
    if isinstance(obj, dict):
        return {k: decimal_to_native(v) for k, v in obj.items()}
    return obj

def filter_params(body):
    movie_description = body["movie_description"] if "movie_description" in body else None
    genre = body["genre"] if "genre" in body else None
    movie_director = body["movie_director"] if "movie_director" in body else None
    release_date = body["release_date"] if  "release_date" in body else None
    ticket_price = body["ticket_price"] if "ticket_price" in body else None
    movie_length = body["movie_length"] if  "movie_length" in body else None
    movie_available = body["movie_available"] if "movie_available" in body else None
    movie_showtimes = body["movie_showtimes"] if "movie_showtimes" in body else None

    movie = {}
    movie['movie_description'] = movie_description
    movie['genre'] = genre
    movie['movie_director'] = movie_director
    movie['release_date'] = release_date
    movie['ticket_price'] = ticket_price
    movie['movie_length'] = movie_length
    movie['movie_available'] = movie_available
    movie['movie_showtimes'] = movie_showtimes

    params = ['movie_description', 'genre', 'movie_director', 'release_date', 'ticket_price', 'movie_length', 'movie_available', 'movie_showtimes']
    filtered_movie = {key: movie[key] for key in params if key in movie and movie[key] is not None}

    return filtered_movie
