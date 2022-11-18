from typing import Union

from .models import CastIn, CastOut, CastUpdate
from .db import casts, database


async def add_cast(payload: CastIn):
    query = casts.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_cast(cast: Union[int, str]):
    if isinstance(cast, int):
        query = casts.select(casts.c.id == cast)
    elif isinstance(cast, str):
        query = casts.select(casts.c.name == cast)
    else:
        raise TypeError("Invalid cast type: %s" % type(cast))
    return await database.fetch_one(query=query)


async def get_all_casts():
    query = casts.select()
    return await database.fetch_all(query=query)