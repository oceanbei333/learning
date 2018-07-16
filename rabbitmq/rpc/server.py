import pika
import traceback


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def on_request(ch, method, props, body):
    n = int(body)
    resp = fib(n)
    print('开始执行任务')
    ch.basic_publish(
        exchange='rpc',
        routing_key=props.reply_to,
        body=str(resp),
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        )
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


conn = None
try:
    credentials = pika.PlainCredentials('admin', 'Password01!')
    conn = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        credentials=credentials,
    ))
    channel = conn.channel()
    channel.exchange_declare(exchange='rpc', exchange_type='direct')
    channel.queue_declare('rpc_queue')
    channel.queue_bind(
        exchange='rpc', queue='rpc_queue', routing_key='rpc_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(consumer_callback=on_request, queue='rpc_queue')
    print('开始监听任务')
    channel.start_consuming()
except:
    traceback.print_exc()
finally:
    if conn:
        print('关闭连接')
        conn.close()