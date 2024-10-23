"""
@Function: the define of session is like to combine all component
@Author : ZhangPeiCheng
@Time : 2024/10/23 19:45
"""
import time
from imp import load_dynamic

from agent.AgentLoader import AgentLoader
from agent.ExpertContext import ExpertContext
from agent.ToolPool import ToolPool


class ExpertSession:

    def __init__(self,loader_conn,model_name,tool_pool,cache_manager,communication_manager,expert_description):
        self.loader_conn = loader_conn
        self.model_name = model_name
        self.tool_pool = tool_pool
        try:
            tool_pool.test_connection()
        except:
            print("tool_pool initialize fail! the session shut down!")
        self.expert_description = expert_description

        self.cache_manager = cache_manager
        self.communication_manager = communication_manager
        self.decomposer = self._decomposer_create()

    def expert_create(self):
        # create agent object to manage the context
        agent_id = self.generate_id()
        expert = ExpertContext(agent_id,self.cache_manager,self.communication_manager,self.loader_conn)
        expert.initial_chat(self.expert_description)
        return expert


    def session_boot(self):

        pass

    def generate_id(self):
        uni_id = str(time.time())[0:5]
        return uni_id

    def _decomposer_create(self):
        # create decomposer
        pass
