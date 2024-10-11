import threading


class BaseAgent:
    def __init__(self, agent_id, rabbitmq_connection, queue_name=None):

        self.agent_id = agent_id
        self.state = 1
        self.current_context = ""
        # ----------------------------------------------communication  ---------------------------------------------
        self.communication_manager = CommunicationManager(rabbitmq_connection, agent_id, queue_name)


    def run_agent(self, human_interp=False):
        """boot the agent"""
        if human_interp:
            prompt = input("Input your prompt: ")
        pass

    def send_message_to_supervisor(self):
        """将任务完成消息发送给Job Supervisor"""
        # 具体实现取决于系统设计
        pass

    def get_context_cache(self):
        """get the context from the cache"""
        pass




class CacheManager:
    def __init__(self, etcdConnection, context):
        self.context = context
        self.etcdConnection = etcdConnection  # client = etcd.Client(host='localhost', port=2379)
        self.echo = 0  # record the echo of the dialogue
        self.cache_key = 0  # record the cache key of the etcd
        self.memory_space = 0


class CommunicationManager:
    def __init__(self, rabbitmq_connection, queue_name, agent_id):
        self.pre_semaphore = []  # pre task semaphore list
        self.post_semaphore = []  # post task resources produce
        self.agent_id = agent_id
        # set the communication queue
        self.rabbitmq_connection = rabbitmq_connection
        self.queue_name = queue_name or f'{agent_id}_queue'
        self.rabbitmq_connection.declare_queue(self.queue_name)

    def send_message(self, to_agent, message):
        """发送消息到指定的agent"""
        print(f"Agent {self.agent_id} sending message to {to_agent.agent_id}")
        self.rabbitmq_connection.send_message(to_agent.queue_name, message)

    def start_listening(self):
        """启动消息接收并处理"""
        def callback(ch, method, properties, body):
            message = body.decode()
            self.message_handler(message)

        threading.Thread(target=self.rabbitmq_connection.receive_message, args=(self.queue_name, callback)).start()
    def message_handler(self, message):
        """消息处理逻辑，具体的逻辑由子类实现"""
        print(f"Agent {self.agent_id} received message: {message}")
