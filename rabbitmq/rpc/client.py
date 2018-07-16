import pika
import uuid


class FibClient(object):

    def __init__(self):
        credentials = pika.PlainCredentials('admin', 'Password01!')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost',
            credentials=credentials,
        ))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='rpc', exchange_type='direct')
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.queue_bind(
            exchange='rpc', queue=self.callback_queue, routing_key=self.callback_queue)
        self.channel.basic_consume(
            self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.exchange_declare(
            exchange='rpc', exchange_type='direct'
        )
        self.channel.basic_publish(
            exchange='rpc',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n)
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fib_client = FibClient()
response = fib_client.call(30)
print(response)