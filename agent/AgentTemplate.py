import threading


class BaseAgent:
    def __init__(self, agent_id, rabbitmq_connection, queue_name=None, etcdConnection=None):
        self.agent_id = agent_id
        self.rabbitmq_connection = rabbitmq_connection
        self.queue_name = queue_name or f'{agent_id}_queue'
        self.etcdConnection = etcdConnection  # client = etcd.Client(host='localhost', port=2379)
        self.global_cache_path = "/agents/global"  # global cache path
        self.local_cache_path = f"/agents/{self.agent_id}/"  # local cache path
        self.state = "initialized"  # label the status of the agent
        self.pre_semaphore = []  # pre task semaphore list
        self.post_semaphore = []  # post task resources produce
        # set the communication queue
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
        # 默认的处理逻辑，可以由子类覆盖
        if message == "task_completed":
            self.semaphore.release()  # 释放信号量，表示前置任务已完成

    def wait_for_dependencies(self):
        """等待所有前驱任务完成"""
        self.semaphore.acquire()

    def execute_task(self, task_data):
        """执行任务的逻辑，由子类实现具体的任务"""
        raise NotImplementedError("This method should be implemented by subclasses")

    def run(self):
        """运行agent，处理消息并执行任务"""
        self.wait_for_dependencies()  # 等待依赖任务完成
        self.execute_task(self.cache.get("task_data"))
        self.send_message_to_supervisor()  # 通知上级任务完成

    def send_message_to_supervisor(self):
        """将任务完成消息发送给Job Supervisor"""
        # 具体实现取决于系统设计
        pass
