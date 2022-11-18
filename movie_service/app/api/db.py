from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)
import os
from databases import Database

# DATABASE_URL = 'postgresql://movies:movies@localhost:5432/movies_db'
DATABASE_URI = os.getenv('DATABASE_URI')
engine = create_engine(DATABASE_URI)
metadata = MetaData()

movies = Table(
    'movies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', ARRAY(String)),
    Column('casts', ARRAY(Integer))
)

database = Database(DATABASE_URI)
