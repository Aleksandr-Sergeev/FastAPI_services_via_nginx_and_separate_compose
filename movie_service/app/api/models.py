from pydantic import BaseModel
from typing import List, Optional, Union


class MovieIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[Union[int, str]]


class MovieOut(MovieIn):
    id: int


class MovieUpdate(MovieIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    casts: Optional[List[int]] = None