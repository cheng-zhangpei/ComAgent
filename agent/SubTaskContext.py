"""
@Function:子任务智能体上下文
@Author : ZhangPeiCheng
@Time : 2024/10/23 20:16
"""
from agent.AgentTemplate import BaseAgent


class SubTaskAgentContext:
    def __init__(self, agent_id, job_description,return_content,
                 cache_manager, tool_pool_ip,tool_pool_port,agent_loader):
        self.agent_id = agent_id
        self.tool_pool_ip = tool_pool_ip
        self.tool_pool_port = tool_pool_port
        self.cache_manager = cache_manager
        self.agent_loader = agent_loader

        self.agent_id = agent_id
        self.job_description = job_description
        self.return_content = return_content
        self.input_memory = f"/agents/{self.agent_id}/input/"
        self.output_memory = f"/agents/{self.agent_id}/output/"
        self.job_memory = f"/agents/{self.agent_id}/jobs/"


    def search_corresponded_call(self,tool_describe):
        pass
    def call_tool(self):
        pass
    def execute(self):
        pass
