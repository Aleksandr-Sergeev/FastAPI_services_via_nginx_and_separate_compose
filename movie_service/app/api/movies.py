from fastapi import APIRouter, HTTPException
from .models import MovieIn, MovieOut
from .db_manager import get_all_movies, get_movie_from_db, add_movie, update_movie, delete_movie
from typing import List, Union
from .service import is_cast_present, create_cast


movies = APIRouter()


@movies.get("/", response_model=List[MovieOut])
async def index():
    return await get_all_movies()


@movies.get("/{movie}", response_model=MovieOut)
async def get_movie(movie: Union[int, str]):
    movie_from_db = await get_movie_from_db(movie)
    if not movie_from_db:
        raise HTTPException(status_code=404,
                            detail=f"Movie {movie} not found")
    return movie_from_db


@movies.post('/', response_model=MovieOut, status_code=201)
async def create_movie(payload: MovieIn):
    for cast in payload.casts:
        if not is_cast_present(cast):
            if isinstance(cast, str):
                cast_response = create_cast(cast)
                print(cast_response)
            else:
                raise HTTPException(status_code=404,
                                    detail=f"Cast with id:{cast} not found")
    # TODO: если актер не в БД casts, надо его туда добавить
    movie_id = await add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }
    return response


@movies.put('/{id}')
async def update_movie(id: int, payload: MovieIn):
    movie = await get_movie_from_db(id)
    if not movie:
        raise HTTPException(status_code=404,
                            detail="Movie with given id not found")
    update_data = payload.dict(exclude_unset=True)
    if 'casts' in update_data:
        for cast in payload.casts:
            if not is_cast_present(cast):
                raise HTTPException(status_code=404,
                                    detail=f"Cast with given id:{cast} not found")
    movie_in_db = MovieIn(**movie)
    updated_movie = movie_in_db.copy(update=update_data)
    return await update_movie(id, updated_movie)


@movies.delete('/{id}')
async def delete_movie(id: int):
    movie = await get_movie_from_db(id)
    if not movie:
        raise HTTPException(status_code=404,
                            detail="Movie not found")
    return await delete_movie(id)
