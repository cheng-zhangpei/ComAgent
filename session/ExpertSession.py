"""
@Function: the define of session is like to combine all component
@Author : ZhangPeiCheng
@Time : 2024/10/23 19:45
"""
import logging
import time
from email.utils import decode_params
from imp import load_dynamic

from fontTools.ttLib.tables.TupleVariation import decompileSharedTuples

from agent.AgentLoader import AgentLoader
from agent.ExpertContext import ExpertContext
from agent.SubClassContext import SubTaskAgentContext
from agent.ToolPool import ToolPool
from agent.prompt_template import llm_output_checkout
from job.Decomposer import Decomposer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
class ExpertSession:

    def __init__(self,loader_conn,cache_manager,communication_manager,expert_description,tool_pool= "" ):
        self.loader_conn = loader_conn
        self.tool_pool = tool_pool
        self.expert_description = expert_description
        self.cache_manager = cache_manager
        self.communication_manager = communication_manager
        self.expert = None
    def expert_create(self):
        # create agent object to manage the context
        agent_id = self.generate_id()
        # create context to manage the process of expert
        expert = ExpertContext(agent_id,self.cache_manager,self.communication_manager,self.loader_conn)
        # the info will remain in the DB, once the history info store in the DB means the agent is create
        response = expert.initial_chat(self.expert_description)
        return expert, response


    def test_components_conn(self):
        agent_loader_conn_test = self.loader_conn.test_conn()
        cache_manager_test= self.cache_manager.test_conn()
        # communication_manager_conn_test = self.communication_manager.test_conn()
        # if agent_loader_conn_test is True and cache_manager_test is True and communication_manager_conn_test is True:
        if agent_loader_conn_test is True and cache_manager_test is True:
            return True
        else:return False

    def session_boot(self,designed_epoch=10,task_description="",talk_model = "no_human"):
        """

        :param designed_epoch: I set the max running epoch
        :param task_description: task description
        :param talk_model: define if human can input or influence the work flow or give addition task
        :return:
        """
        # a loop will cover the work flow until we stop the running of the sys
        # one loop corespondent with one single task, if wanna the whole session always run in the k8s
        # we need to design a lot of web hook or something else to drive the running this function
        initial_echo = designed_epoch
        expert_output = ""
        human_ = False
        if talk_model == "no_human":
            human_ = True
        if self.test_components_conn() is False:
            logger.error("Some indispensable component is unavailable!")

        while designed_epoch > 0:
            if designed_epoch == initial_echo:
                self.expert, response = self.expert_create()
            else:
                if human_ is False:
                    response = self.expert.task_input_info(task_description)
                else:
                    human_input = input("please enter the info")
                    response = self.expert.task_input_info(human_input)
            # 1. test if all the components are available
                #->  we should set test function for all components

            # 2. give your task to expert

            # 3. pass(if pass the check out) response to job
            # job = Decomposer(expert_output,self.loader_conn,self.cache_manager,self.communication_manager)

            # 4. pass the result of decomposing to  expert to create sub-task agent


            # todo: 等到cache manager 和 communication manager全部完成之后再进行开发
            # job = self._decomposer_create(clean_data_json)
              # => generate sub-task agent

              # => run the DAG task map

              # => collect the info of running.the running is under supervise by the JobSupervisor

              # => let the expert decide

            # 5. gain the response of the execution(so all the task will be done by the expert)
                # => pass the info to the  expert
            designed_epoch -= 1



        pass

    def generate_id(self):
        uni_id = str(time.time())[0:5]
        return uni_id

    def _decomposer_create(self,expert_input):
        # create job
        decomposer = Decomposer(expert_input)
        return decomposer
