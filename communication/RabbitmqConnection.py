"""
@author        :ZhangPeiCheng
@function      :
@time          :2024/9/26 20:44
"""
import pika


class RabbitMQConnection:
    def __init__(self, host='localhost',port=5555, exchange='agent_exchange'):
        self.host = host
        self.port = port
        self.exchange = exchange
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,port=self.port))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

    def declare_queue(self, queue_name):
        """声明队列并绑定到交换机"""
        self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=queue_name)

    def send_message(self, routing_key, message):
        """发送消息到指定的队列"""
        self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=message)

    def receive_message(self, queue_name, callback):
        """从队列接收消息并处理"""
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f'Started consuming messages from {queue_name}')
        self.channel.start_consuming()

    def close(self):
        """关闭连接"""
        self.connection.close()
