import threading


class BaseAgent:
    def __init__(self, agent_id, cache_manager, communication_manager,agent_loader):
        self.agent_id = agent_id
        self.state = 1
        self.current_context = ""
        self.cache_manager = cache_manager
        self.communication_manager = communication_manager
        self.agent_loader = agent_loader
        self.global_cache = "/global_cache"
        self.agent_cache_key = f"/{agent_id}"

    def run_agent(self, human_interp=False):
        """boot the agent"""
        if human_interp:
            prompt = input("Input your prompt: ")

        pass

    def send_message_to_supervisor(self):
        pass

    def get_context_cache(self):
        """get the context from the cache"""
        pass





class CommunicationManager:
    def __init__(self, rabbitmq_connection, queue_name, agent_id):
        self.pre_semaphore = []  # pre task semaphore list
        self.post_semaphore = []  # post task resources produce
        self.agent_id = agent_id
        self.rabbitmq_connection = rabbitmq_connection
        self.queue_name = queue_name or f'{agent_id}_queue'
        self.rabbitmq_connection.declare_queue(self.queue_name)

    def send_message(self, to_agent, message):
        print(f"Agent {self.agent_id} sending message to {to_agent.agent_id}")
        self.rabbitmq_connection.send_message(to_agent.queue_name, message)

    def start_listening(self):
        def callback(ch, method, properties, body):
            message = body.decode()
            self.message_handler(message)

        threading.Thread(target=self.rabbitmq_connection.receive_message, args=(self.queue_name, callback)).start()
    def message_handler(self, message):
        print(f"Agent {self.agent_id} received message: {message}")
