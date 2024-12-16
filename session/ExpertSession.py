"""
@Function: the define of session is like to combine all component
@Author : ZhangPeiCheng
@Time : 2024/10/23 19:45
"""
import json
import logging
import time
from agent.expert_context import ExpertContext
from agent.OutInfoManager import OutInfoManager
from cache.LocalCache import json_str
from job.decomposer import Decomposer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
class ExpertSession:

    def __init__(self,loader_conn,cache_manager,expert_description,tool_pool= "" ):
        self.loader_conn = loader_conn
        self.tool_pool = tool_pool
        self.expert_description = expert_description
        self.cache_manager = cache_manager
        self.expert = None
        self.decomposer = Decomposer(self.loader_conn,self.cache_manager)
    def expert_create(self):
        # create agent object to manage the context
        agent_id = self.generate_id()
        # create context to manage the process of expert
        expert = ExpertContext(agent_id,self.cache_manager,self.loader_conn)
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

    def session_boot(self,designed_epoch=10,human_interp = True,task_description=""):
        """

        :param designed_epoch: I set the max running epoch
        :param task_description: task description
        :param talk_model: define if human can input or influence the work flow or give addition task
        :return:
        """
        # a loop will cover the work flow until we stop the running of the sys
        # one loop corespondent with one single task, if wanna the whole session always run in the k8s
        # we need to design a lot of web hook or something else to drive the running this function
        infinite = False
        isFirst = True
        if designed_epoch == -1:
            infinite = True
        # 1. test if all the components are available
        # ->  we should set test function for all components
        if self.test_components_conn() is False:
            logger.error("Some indispensable component is unavailable!")
        # 2. give your task to expert
        while designed_epoch > 0 or infinite is True:
            logger.info(f"current epoch {designed_epoch}")
            if isFirst:
                self.expert, response = self.expert_create()
                logger.info(response)
                isFirst = False
            # not the first epoch
            if human_interp == True:
                # if human interp
                human_input = input("please enter the info: ")
                response = self.expert.task_input_info(human_input)
            else:
                outInfoManager = OutInfoManager()
                model_input = outInfoManager.gain_info()
                response = self.expert.task_input_info(model_input)
           # 4. pass the result of decomposing to  expert to create sub-task agent and execute
        # 先调任务图
            logger.info(response)
            result = self.decomposer.tasks_execute(response)


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
