from pika import BlockingConnection, ConnectionParameters


# async def on_message(message: IncomingMessage):
#     txt = message.body.decode("utf-8")
#     print(json.loads(txt))


def test_queue_connection(channel) -> None:
    if channel:
        channel.basic_publish(exchange='',
                              routing_key='from_casts',
                              body='Hello World!')


def main():
    connection = BlockingConnection(ConnectionParameters("localhost"))
    # connection = await connect("amqp://guest:guest@localhost/", loop = loop)
    channel = connection.channel()
    queue_from_casts = channel.queue_declare("from_casts")
    queue_from_movies = channel.queue_declare("from_movies")
    test_queue_connection(channel)

    # queue.consume(on_message, no_ack = True)


# if __name__ == "__main__":
#