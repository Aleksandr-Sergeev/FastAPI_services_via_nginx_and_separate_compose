from fastapi import APIRouter
from fastapi.routing import Request
from .schema import MessageSchema

rmq_router = APIRouter()


@rmq_router.post('/send-message')
async def send_message(payload: MessageSchema, request: Request):
    request.app.pika_client.send_message(
        {"message": payload.message}
    )
    return {"status": "ok"}
