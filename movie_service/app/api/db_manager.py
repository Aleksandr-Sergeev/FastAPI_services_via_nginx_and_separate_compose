from api.models import MovieIn
from api.db import movies, database


async def add_movie(payload: MovieIn):
    query = movies.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_all_movies():
    query = movies.select()
    return await database.fetch_all(query=query)


async def get_movie_from_db(movie):
    if isinstance(movie, int):
        query = movies.select(movies.c.id == movie)
    elif isinstance(movie, str):
        query = movies.select(movies.c.name == movie)
    return await database.fetch_one(query=query)


async def delete_movie(id: int):
    query = movies.delete().where(movies.c.id == id)
    return await database.execute(query=query)


async def update_movie(id: int, payload: MovieIn):
    query = (
        movies
        .update()
        .where(movies.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)


