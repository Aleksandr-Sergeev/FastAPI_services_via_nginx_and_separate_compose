from fastapi import APIRouter, HTTPException
from typing import List, Union
from .models import CastOut, CastIn, CastUpdate
from .db_manager import add_cast, get_all_casts, get_cast as get_cast_from_db


casts = APIRouter()


@casts.post('/', response_model=CastOut, status_code=201)
async def create_cast(payload: CastIn):
    cast_id = await add_cast(payload)
    response = {
        'id': cast_id,
        **payload.dict()
    }
    return response


@casts.get('/{cast}/', response_model=CastOut)
async def get_cast(cast: Union[int, str]):
    cast_in_db = await get_cast_from_db(cast)
    if not cast_in_db:
        raise HTTPException(status_code=404, detail="Cast not found")
    return cast_in_db


@casts.get('/', response_model=List[CastOut])
async def index():
    return await get_all_casts()
