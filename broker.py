import pika

# The broker class creates a connection to RabbitMQ,
# creates a channel, creates a queue, and then can send and receives
# messages
class Broker(object):
    def __init__(self, exchange_name="meter") -> None:
        self.exchange = exchange_name
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self._channel = self._connection.channel()
        # self._channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
        self._channel.queue_declare(queue="meterValues")

    def send(self, payload, routing_key="meterValues") -> None:
        """
        The function takes a payload and a routing key as arguments and publishes the payload to
        the RabbitMQ server using the routing key

        :param payload: The message to send
        :param routing_key: The routing key is how the exchange decides which queue to send the message to,
        defaults to meterValues (optional)
        """
        self._channel.basic_publish(exchange="", routing_key=routing_key, body=payload)
        print(f"Msg sent: {payload}")

    def set_receive_callback(self, callback, queue="meterValues", ack=True) -> None:
        """
        It sets the callback function for the queue.

        :param callback: The function to call when a message is received
        :param queue: The name of the queue to listen to, defaults to meterValues (optional)
        :param ack: If True, the callback will be called with the message as the first parameter and a
        function to acknowledge the message as the second parameter. If False, the callback will be
        called with the message as the only parameter, defaults to True (optional)
        """
        # result = self._channel.queue_declare(queue='', exclusive=True)
        # queue_name = result.method.queue
        self._channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=ack
        )

    def receive(self) -> None:
        """
        Starts consuming messages from the queue
        """
        print("Receiving data...")
        self._channel.start_consuming()
