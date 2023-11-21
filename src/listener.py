import pika
import os
import sys
import ssl
import boto3

rmqHost = os.environ.get('RMQ_HOST', 'localhost')
rmqUser = os.environ.get('RMQ_USER', 'guest')

rmqVHost = os.environ.get('RMQ_VHOST', '/')
rmqPort = int(os.environ.get('RMQ_PORT', '5671'))
rmqQueue = os.environ.get('RMQ_QUEUE', 'hello')
rmqExchange = os.environ.get('RMQ_EXCHANGE', '')

# Get rmqPass from AWS Secrets Manager

# Create a Secrets Manager client
secrets_manager = boto3.client('secretsmanager')

# Retrieve the secret value
response = secrets_manager.get_secret_value(SecretId='your_secret_id')

# Extract the password from the response
rmqPass = response['SecretString']

# Use the rmqPass variable in your code



cxt = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_options = pika.SSLOptions(context=cxt, server_hostname=rmqHost)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rmqHost, port=rmqPort, virtual_host=rmqVHost, credentials=pika.PlainCredentials(rmqUser, rmqPass), ssl_options=ssl_options))
channel = connection.channel()


# Create a queue
queue = channel.queue_declare(queue='my_queue')

# Create a consumer
consumer = channel.basic_consume(
    queue=queue,
    on_message_callback=on_message,
    auto_ack=True
)

# Start consuming messages
channel.start_consuming()

def on_message(ch, method, properties, body):
    # Do something with the message
    print(body)

    # Acknowledge the receipt of the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Wait for messages
print('Waiting for messages. To exit press CTRL+C')

# Close the connection
connection.close()
