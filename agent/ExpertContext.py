"""
@Function:专家智能体上下文
@Author : ZhangPeiCheng
@Time : 2024/10/23 20:16
"""
from agent.AgentTemplate import BaseAgent


class ExpertContext:
    def __init__(self, agent_id, rabbitmq_connection, queue_name=None):
        # 继承agent类模板
        BaseAgent.__init__(self, agent_id, rabbitmq_connection, queue_name=None)

