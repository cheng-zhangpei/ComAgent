

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




