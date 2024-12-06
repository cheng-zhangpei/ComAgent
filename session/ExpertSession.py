"""
@Function: the define of session is like to combine all component
@Author : ZhangPeiCheng
@Time : 2024/10/23 19:45
"""
import logging
import time
from imp import load_dynamic

from agent.AgentLoader import AgentLoader
from agent.ExpertContext import ExpertContext
from agent.ToolPool import ToolPool

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
class ExpertSession:

    def __init__(self,loader_conn,cache_manager,communication_manager,expert_description,tool_pool= "" ):
        self.loader_conn = loader_conn
        self.tool_pool = tool_pool
        self.expert_description = expert_description
        self.cache_manager = cache_manager
        self.communication_manager = communication_manager
        # self.decomposer = self._decomposer_create()

    def expert_create(self):
        # create agent object to manage the context
        agent_id = self.generate_id()
        # create context to manage the process of expert
        expert = ExpertContext(agent_id,self.cache_manager,self.communication_manager,self.loader_conn)
        # the info will remain in the DB, once the history info store in the DB means the agent is create
        expert.initial_chat(self.expert_description)
        return expert

    def test_components_conn(self):
        agent_loader_conn_test = self.loader_conn.test_conn()
        cache_manager_test= self.cache_manager.test_conn()
        communication_manager_conn_test = self.communication_manager.test_conn()
        if agent_loader_conn_test is True and cache_manager_test is True and communication_manager_conn_test is True:
            return True
        else:return False
    def llm_output_checkout(self,raw_data):
        # try to clean the formation of model`s output


        return ""

    def session_boot(self,task_description="",talk_model = "no_human"):
        """

        :param task_description: task description
        :param talk_model: define if human can input or influence the work flow or give addition task
        :return:
        """
        # a loop will cover the work flow until we stop the running of the sys
        # one loop corespondent with one single task, if wanna the whole session always run in the k8s
        # we need to design a lot of web hook or something else to drive the running this function
        # so how can we stop the process?
        expert = self.expert_create()
        task_input = task_description
        expert_output = ""
        human_ = False
        if talk_model == "no_human":
            human_ = True
        else:
            expert_output = expert.input_info(task_input)
        while True:
            # 1. test if all the components are available
                #->  we should set test function for all components
            if self.test_components_conn():
                logger.error("Some indispensable component is unavailable!")
                break
            # 2. give your task to expert
            if human_ is True:
                human_input = input("please enter the info")
                expert_output = expert.input_info(human_input)
            # 3. examine the response from the expert and pass(if pass the check out) response to decomposer
            clean_data_json = self.llm_output_checkout(expert_output)
            # 4. pass the result of decomposing to  expert to create sub-task agent

            # 5. gain the response of the execution(so all the task will be done by the expert)

            # 6. ask for human input( optional ) / next input



        pass

    def generate_id(self):
        uni_id = str(time.time())[0:5]
        return uni_id

    def _decomposer_create(self):
        # create decomposer
        pass
