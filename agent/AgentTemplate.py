import threading


class BaseAgent:
    def __init__(self, agent_id, rabbitmq_connection, queue_name=None, etcdConnection=None, tool_server_ip="localhost",
                 tool_server_port="8888"):

        self.agent_id = agent_id
        self.state = "initialized"  # label the status of the agent\
        self.current_context = ""  # it will record the current context
        self.cache_manager = CacheManager(etcdConnection, self.agent_id, self.current_context)
        # ----------------------------------------------communication  ---------------------------------------------
        self.communication_manager = CommunicationManager(rabbitmq_connection, agent_id, queue_name)
        # ----------------------------------------------tool server ---------------------------------------------
        self.tool_server = ToolServer(tool_server_ip, tool_server_port)

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


class ToolServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.tool_config_list = {}

    def get_config_list(self):
        """get the info of the tool server"""

        # send the request
        pass


class CacheManager:
    def __init__(self, etcdConnection, agent_id, context):
        self.context = context
        self.etcdConnection = etcdConnection  # client = etcd.Client(host='localhost', port=2379)
        self.global_cache_path = "/agents/global"  # global cache path
        self.local_cache_path = f"/agents/{agent_id}/"  # local cache path
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
