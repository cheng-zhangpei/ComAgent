"""
@Function:专家智能体上下文
@Author : ZhangPeiCheng
@Time : 2024/10/23 20:16
"""
import json
import logging
import re

from agent.prompt_template import initial_prompt_expert, json_encode, expert_task_prompt

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ExpertContext:
    def __init__(self, agent_id, cache_manager,agent_loader):
        # 继承agent类模板
        self.echo = 0 # record current epoch of the speech
        self.agent_id = agent_id
        self.local_cache_prefix = f"/{agent_id}"
        self.local_cache_key = ""
        self.global_cache = "/global_cache"
        self.cache_manager = cache_manager
        self.agent_loader = agent_loader
        self.memory_space = 5
        self.retry = 2
        self.input_memory = f"/agents/{self.agent_id}/input/"
        self.output_memory = f"/agents/{self.agent_id}/output/"
        self.job_memory = f"/agents/{self.agent_id}/jobs/"


    def initial_chat(self,init_task_description):
        # format the input
        retry_count = self.retry
        initial_input= initial_prompt_expert(init_task_description)
        # create memory space
        response = self.agent_loader.send_message(initial_input, 200)
        response_str = self.postprocess_output(str(response))
        self.echo += 1
        self.cache_manager.write_task(self.input_memory + f"{self.echo}",init_task_description, self.agent_id) # the info writed here is not right
        self.cache_manager.write_task(self.output_memory + f"{self.echo}",response_str, self.agent_id) # the info writed here is not right
        logger.info(f"memory space created(the info is key):\n"
                    f"input memory:{self.input_memory}\n"
                    f"output memory:{self.output_memory}\n"
                    f"job memory： {self.job_memory}\n")
        return response_str


    def task_input_info(self,input_info):

        # todo 模型输入信息，并读取之前的输出，这一点其实是固定的，如果正常创建，记忆空间中一定会有该模型，否则其实可以丢一个警告
        # read memory space
        memory = self.memory_space
        epoch = self.echo
        hist = None
        while epoch > 0:
            if memory > 0:
                # todo :search functions
                current_key_1 = self.output_memory + f"{epoch}"
                current_key_2 = self.input_memory + f"{epoch}"
                logger.info(f"current key1 {current_key_1}")
                logger.info(f"current key2 {current_key_2}")
                hist_out = self.cache_manager.get_memory(current_key_1)
                hist_in = self.cache_manager.get_memory(current_key_2)
                hist = "任务memory：" + hist_in + "输出memory：" + hist_out
                logger.info(f"memory hist {epoch}: " + hist)
            epoch -= 1
            memory -= 1
        # combine the info
        cleaned_response = None
        if hist is not None:
            prompt_ = expert_task_prompt(input_info, str(hist),"None")
            # get the response from  the model
            response = self.agent_loader.send_message(prompt_,700)
            cleaned_response = json_encode(response)
        else:
            logger.error("the agent did not initialized!")
        return cleaned_response



    def job_schedule_input_info(self,task_status):
        # the output of initial
        pass

    def postprocess_output(self,text):
        """
        后处理生成文本，去除冗余信息
        """
        # 去除多余的空格和换行
        text = re.sub(r"\s+", " ", text).strip()
        # 去除重复的句子
        sentences = text.split("。")
        unique_sentences = list(dict.fromkeys(sentences))  # 去重
        return "。".join(unique_sentences)

