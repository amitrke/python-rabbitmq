import pika

connection = pika.BlockingConnection()
channel = connection.channel()

# Create a queue
queue = channel.queue_declare(queue='my_queue')

# Create a consumer
consumer = channel.basic_consume(
    queue=queue,
    on_message_callback=on_message,
    auto_ack=False
)

# Start consuming messages
channel.start_consuming()

def on_message(ch, method, properties, body):
    # Do something with the message
    print(body)

    # Acknowledge the receipt of the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Close the connection
connection.close()
