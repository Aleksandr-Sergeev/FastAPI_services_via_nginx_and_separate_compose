from fastapi import FastAPI
from api.movies import movies
from api.db import metadata, database, engine
import uvicorn
from rmq.rmq_queue import PikaClient
from app.rmq.rmq_router import rmq_router


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    def log_incoming_message(cls, message: dict):
        """Method to do something meaningful with the incoming message"""
        # logger.info('Here we got incoming message %s', message)


metadata.create_all(engine)

# app = FastAPI()
app = App(openapi_url="/api/v1/movies/openapi.json", docs_url="/api/v1/movies/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(movies,
                   prefix='/api/v1/movies',
                   tags=['movies'])

app.include_router(rmq_router,
                   tags=['rmq'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)