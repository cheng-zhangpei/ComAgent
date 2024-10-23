"""
@Function:子任务智能体上下文
@Author : ZhangPeiCheng
@Time : 2024/10/23 20:16
"""
from agent.AgentTemplate import BaseAgent


class SubTaskAgentContext:
    def __init__(self, agent_id,  cache_manager, communication_manager, tool_pool_ip,tool_pool_port):
        BaseAgent.__init__(self, agent_id, cache_manager, communication_manager)
        self.tool_pool_ip = tool_pool_ip
        self.tool_pool_port = tool_pool_port
    def call_tool(self):
        """工具调用"""
        pass
