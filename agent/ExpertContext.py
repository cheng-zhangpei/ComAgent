"""
@Function:专家智能体上下文
@Author : ZhangPeiCheng
@Time : 2024/10/23 20:16
"""
from agent.AgentTemplate import BaseAgent
from agent.prompt_template import expert_agent_prompt


class ExpertContext:
    def __init__(self, agent_id, cache_manager, communication_manager,agent_loader):
        # 继承agent类模板
        self.base = BaseAgent.__init__(self, agent_id, cache_manager, communication_manager,agent_loader)
        self.echo = 0 # record the epoch of the speech
    def initial_chat(self,init_task_description):
        # format the input
        initial_prompt = expert_agent_prompt(init_task_description,self.base.global_cache,self.base.agent_cache_key)
        # create memory space
        response = self.base.agent_loader.send_message(initial_prompt)
        self.base.cache_manager.write( self.base.agent_cache_key+f"/{self.echo}", response)
    def input_info(self,input_info):
        # todo 模型输入信息，并读取之前的输出，这一点其实是固定的，如果正常创建，记忆空间中一定会有该模型，否则其实可以丢一个警告
        pass
