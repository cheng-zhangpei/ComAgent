"""
@author        :ZhangPeiCheng
@function      :
@time          :2024/10/11 15:54
"""
import time

import networkx as nx

from agent.SubClassContext import SubTaskAgentContext
from job.JobSupervisor import JobSupervisor


class Decomposer:
    """
    create sub-task agent and optimized the work flow of the agent:
    """

    def __init__(self, expert_output,loader_conn,cache_manager,communication_manager):
        self.expert_input = expert_output
        self.DAG = None
        self._init_DAG() # the schedule graph will across the whole process
        self.agent_id_list = []
        self.cache_manager = cache_manager
        self.communication_manager = communication_manager
        self.loader_conn = loader_conn
        self.sub_task_agent_list = [] # that is the job list changed with job
        self.job_supervisor = JobSupervisor()
    def _sub_task_agent_create(self):
        agent_id = self.generate_id()
        sub_task_agent = SubTaskAgentContext(agent_id, self.cache_manager,
                                             self.communication_manager, "127.0.0.1",9956, self.loader_conn)
        return sub_task_agent

    def _message_parser(self):
        """
        parse the expert output
        """

        # all the info of the agent will keep in main memory

        # convert the output into the json format

        # get the dependency relations

        # get the info of the agent

        pass



    def _init_DAG(self):
        """
        initialize the DAG。we just need to use the id of the agent to create the DAG network
        :return:
        """
        pass

    def load_agent(self):
        """
        load the agent into the DAG
        Using topological sorting order for agent loading
        :return:
        """

    def generate_id(self):
        uni_id = str(time.time())[0:5]
        return uni_id

    def task_schedule(self):
        # todo the job assign to the sub-task agent can not promised to be finished in a single function
        # todo so I try to come up with a mechanism to schedule the task dynamically or divide the job to fined-grain

        pass



