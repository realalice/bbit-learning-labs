import pika
import os

class mqProducer():
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        # Save parameters to class variables
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.setupRMQConnection()
        # Call setupRMQConnection

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        connection = pika.BlockingConnection(parameters=con_params)

        # Establish Channel
        channel = connection.channel()
        self.channel = channel

        # Create the exchange if not already present
        if (self.exchange_name != None):
            self.exchange = channel.exchange_declare(self.exchange_name)

    def publishOrder(self, message: str) -> None:
        # Basic Publish to Exchange
        channel = self.channel
        channel.basic_publish(
            exchange = self.exchange_name,
            routing_key = self.routing_key,
            body = message,
        )