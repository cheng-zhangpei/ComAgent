"""
@Function:子任务智能体上下文
@Author : ZhangPeiCheng
@Time : 2024/10/23 20:16
"""
from click import prompt

from agent.AgentTemplate import BaseAgent
from agent.prompt_template import sub_task_agent_server_prompt, json_encode, sub_task_agent_response_prompt


class SubTaskAgentContext:
    def __init__(self, agent_id, task_description,return_content,
                 cache_manager, tool_pool,agent_loader):
        self.agent_id = agent_id
        self.tool_pool = tool_pool


        self.cache_manager = cache_manager
        self.agent_loader = agent_loader

        self.agent_id = agent_id
        self.task_description = task_description
        self.return_content = return_content
        # 结果记忆空间，供后来的智能体进行调用
        self.result_memory = f"/agents/{self.agent_id}/result/"
        # 中间过程记忆空间
        self.process_memory = f"/agents/{self.agent_id}/process/"

    def search_corresponded_call(self,tool_describe):
        # todo 需要等待数据库的搜索功能完善之后再来做这个功能
        pass
    """
    @Function:工具调用
    """
    def call_tool(self,tool_call):

        pass
    """
    @Function: 获得指定空间中的工具信息
    """
    def gain_tool_config(self,tool_path):

        return ""
    """
    @Function: 执行任务
    """
    def execute(self,prefix_ids):
        # 从数据库中获取上一个前驱结点的信息
        pre_execute_result = ""
        for id in prefix_ids:
            hist_path =  f"/agents/{id}/result/"
            pre_execute_result += self.cache_manager.get_memory(hist_path)
        # 构建Tool Server type 信息
        tool_servers = self.tool_pool.get_tool_servers()
        prompt1 = sub_task_agent_server_prompt(tool_servers,self.task_description,self.return_content)
        # 获取初步步骤
        server_des_response = self.agent_loader.send_message(prompt1)
        server_des_response = json_encode(server_des_response)
        # 对每一个子任务进行决策
        for sub_task in server_des_response["jobs"]:
            # 在执行过程中的数据会被缓存在数据库中
            self.execute_sub_task(sub_task)
        # 对运行中数据进行汇总
        process_memory = self.cache_manager.get_by_prefix(self.process_memory)
        prompt3 = sub_task_agent_response_prompt(process_memory,self.return_content)
        submit_response = self.agent_loader.send_message(prompt3)
        result = self.submit_summary(submit_response)
        # todo:判断任务执行状态，如果任务状态异常，需要回滚重新决策

        return result
    def execute_sub_task(self,sub_task):
        pass
    def submit_summary(self,sub_task_response):
        pass