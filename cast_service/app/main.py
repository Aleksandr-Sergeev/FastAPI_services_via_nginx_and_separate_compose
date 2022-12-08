import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger

from api.casts import casts
from api.db import metadata, database, engine
from app.rmq.rmq_queue import PikaClient
from app.rmq.rmq_router import rmq_router


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    def log_incoming_message(cls, message: dict):
        """Method to do something meaningful with the incoming message"""
        logger.info('Here we got incoming message %s', message)


metadata.create_all(engine)

# app = FastAPI(openapi_url="/api/v1/casts/openapi.json", docs_url="/api/v1/casts/docs")
app = App(openapi_url="/api/v1/casts/openapi.json", docs_url="/api/v1/casts/docs")
app.include_router(rmq_router,
                   tags=['rmq'])
app.include_router(casts,
                   prefix='/api/v1/casts',
                   tags=['casts'])


@app.on_event("startup")
async def startup():
    await database.connect()
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
