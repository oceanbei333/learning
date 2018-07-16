from celery import Celery
RABBITMQ_IP = "127.0.0.1"
RABBITMQ_PORT = "5672"
RABBITMQ_USER = ""
RABBITMQ_PASS = ""
app = Celery(
    backend='amqp',
    broker='amqp://{}:{}@{}:{}'.format(
        RABBITMQ_USER,
        RABBITMQ_PASS,
        RABBITMQ_IP,
        RABBITMQ_PORT,
    ),
    CELERY_ROUTES={
        'worker.test1': {
            'queue': 'test1'
        },
        'worker.test2': {
            'queue': 'test2'
        },
        'worker.test3': {
            'queue': 'test3'
        },
    },
)
