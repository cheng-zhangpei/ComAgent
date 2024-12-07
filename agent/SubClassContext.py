"""
@Function:子任务智能体上下文
@Author : ZhangPeiCheng
@Time : 2024/10/23 20:16
"""
from agent.AgentTemplate import BaseAgent


class SubTaskAgentContext:
    def __init__(self, agent_id,  cache_manager, communication_manager,
                 tool_pool_ip,tool_pool_port,agent_loader):
        self.tool_pool_ip = tool_pool_ip
        self.tool_pool_port = tool_pool_port
        self.cache_manager = cache_manager
        self.agent_loader = agent_loader
        self.communication_manager = communication_manager

        self.echo = 0  # record current epoch of the speech
        self.agent_id = agent_id
        self.local_cache_prefix = f"/{agent_id}"
        self.local_cache_key = ""
        self.global_cache = "/global_cache"

        self.prefix_agent_id = None


    def search_corresponded_call(self,tool_describe):
        pass

    def call_tool(self):
        pass
    def task_info_input(self):
        pass
