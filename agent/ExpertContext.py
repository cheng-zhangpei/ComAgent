"""
@Function:专家智能体上下文
@Author : ZhangPeiCheng
@Time : 2024/10/23 20:16
"""
import json
import logging

from agent.AgentTemplate import BaseAgent
from agent.prompt_template import expert_agent_prompt, clean_and_parse
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ExpertContext:
    def __init__(self, agent_id, cache_manager, communication_manager,agent_loader):
        # 继承agent类模板
        self.echo = 0 # record current epoch of the speech
        self.agent_id = agent_id
        self.local_cache_prefix = f"/{agent_id}"
        self.local_cache_key = ""
        self.global_cache = "/global_cache"
        self.cache_manager = cache_manager
        self.agent_loader = agent_loader
        self.communication_manager = communication_manager
        self.memory_space = 3
        self.retry = 2


    def initial_chat(self,init_task_description):
        # format the input
        retry_count = self.retry
        initial_prompt = expert_agent_prompt(init_task_description,"it is initial chat!",self.global_cache)
        # create memory space
        response = self.agent_loader.send_message(initial_prompt)
        self.local_cache_key= self.local_cache_prefix + f"/{self.echo}"
        self.echo += 1
        cleaned_response = clean_and_parse(response['result'])
        serialized_data = ""
        if cleaned_response == 'error':
            logger.info("parse error! start retry again")
            # parse error retry
            while retry_count :
                response = self.agent_loader.send_message(initial_prompt)
                cleaned_response = clean_and_parse(response['result'])
                # here we just save the memory part
                if cleaned_response != 'error':
                    serialized_data = json.dumps(cleaned_response, ensure_ascii=False)
                    break
                retry_count -= 1
        else:
            serialized_data = json.dumps(cleaned_response, ensure_ascii=False)
        # cleaned_response = json.loads(serialized_data) # str -> json
        print("write key")
        print(self.local_cache_key)
        # in convert process you need to transform the formation
        self.cache_manager.write_agent_cache(json.dumps(json.loads(serialized_data)['memory'], ensure_ascii=False)
                                             , self.agent_id) # the info writed here is not right
        return cleaned_response


    def task_input_info(self,input_info):

        # todo 模型输入信息，并读取之前的输出，这一点其实是固定的，如果正常创建，记忆空间中一定会有该模型，否则其实可以丢一个警告
        # read memory space
        memory = self.memory_space
        epoch = self.echo
        hist = None
        while epoch > 0:
            if memory > 0:
                current_key_ = self.local_cache_prefix + f"/{epoch}"
                print("current key")
                print(current_key_)
                hist = self.cache_manager.get(current_key_)
                cleaned_response = json.loads(hist)  # str -> json
                print(cleaned_response)
            epoch -= 1
            memory -= 1
        # combine the info
        if hist is not None:
            # combine todo: more formation of tasks and you should construct more prompt formats

            pass
        prompt_ = expert_agent_prompt(input_info,str(hist),self.global_cache)
        # get the response from  the model
        response = self.agent_loader.send_message(prompt_)
        cleaned_response = clean_and_parse( response['result'])
        print(cleaned_response)
        # write into it`s memory space

        # return the response



        pass
    def job_schedule_input_info(self,task_status):
        # the output of initial
        pass


