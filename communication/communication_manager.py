"""
@Function:
@Author : ZhangPeiCheng
@Time : 2024/12/7 18:26
"""
import logging
import socket
import threading
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CrossCommunicationManager:
    def __init__(self, rabbitmq_connection):
        self.rabbitmq_connection = rabbitmq_connection


class CommunicationManager:
    """the communication manager is to manager the communication network of the expertSession"""
    def __init__(self, rabbitmq_connection):
        self.rabbitmq_connection = rabbitmq_connection
    def test_conn(self):
        try:
            with socket.create_connection((self.etcd_ip, self.etcd_port), timeout=5) as sock:
                logger.info(f"CacheManager Connection to {self.etcd_ip}:{self.etcd_port} is successful.")
                return True
        except socket.timeout:
            logger.info(f"CacheManager Connection to {self.etcd_ip}:{self.etcd_port} timed out.")
            return False
        except socket.error as e:
            logger.info(f"CacheManager Connection to {self.etcd_ip}:{self.etcd_port} failed: {e}")
            return False


class CommunicationUnit:
    """manage the communication session between 2 agent"""
    def __init__(self, rabbitmq_connection, queue_name, source_ip, des_ip):
        self.send_id = source_ip
        self.des_ip = des_ip
        self.queue_name = queue_name
        self.rabbitmq_connection = rabbitmq_connection
        self.rabbitmq_connection.declare_queue(self.queue_name)

    def send_message(self, to_agent, message):
        print(f"Agent {self.send_id} sending message to {to_agent.des_ip}")

        self.rabbitmq_connection.send_message(to_agent.queue_name, message)

    def start_listening(self):
        def callback(ch, method, properties, body):
            message = body.decode()
            self.message_handler(message)
        threading.Thread(target=self.rabbitmq_connection.receive_message, args=(self.queue_name, callback)).start()

    def message_handler(self, message):
        print(f"Agent {self.send_id} received message: {message}")
