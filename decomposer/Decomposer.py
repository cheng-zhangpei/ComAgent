"""
@author        :ZhangPeiCheng
@function      :
@time          :2024/10/11 15:54
"""
import networkx as nx


class Decomposer:
    """
    create sub-task agent and optimized the work flow of the agent:
    """

    def __init__(self, expert_input):
        self.expert_input = expert_input
        self.dag = nx.DiGraph() # initialize the DiGraph
        self.agent_id_list = []
        self.description_list = []
        self.parameters_list = []
        self.parameter_description = []
        self.cache_key_list_local = []
        self.cache_key_global = ""


    def message_parser(self):
        """
        parse the expert output
        """
        # all the info of the agent will keep in main memory
        dependency = []
        description = ""
        cache_key_1 = ""
        cache_key_2 = ""
        tool_address= ""
        parameters = {}
        # convert the output into the json format

        # get the dependency relations

        # get the info of the agent
        agent_parameter(dependency,description,cache_key_1,cache_key_2,tool_address,parameters)
        pass


    def create_sub_task_agent(self):
        """
        create sub-task agent
        :return:
        """
        pass


    def init_DAG(self):
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


class agent_parameter:
    """
    稍微封装一下装载器
    """
    def __init__(self, dependency, description, cache_key_1, cache_key_2, tool_address, parameters):
        self.dependency = dependency
        self.description = description
        self.cache_key_1 = cache_key_1
        self.cache_key_2 = cache_key_2
        self.tool_address = tool_address
        self.parameters = parameters
