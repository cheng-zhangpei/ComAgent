"""
@author        :ZhangPeiCheng
@function      :
@time          :2024/10/11 15:54
"""
import time
from collections import deque, defaultdict
from sre_constants import error

import networkx as nx
from scipy.stats import describe
from torch.fx.experimental.accelerator_partitioner import DAGNode

from agent.sub_task_agent_context import SubTaskAgentContext
from job.job_supervisor import JobSupervisor


class Decomposer:
    """
    create sub-task agent and optimized the work flow of the agent:
    """
    def __init__(self,loader_conn,cache_manager):
        self.expertId = ""
        self.DAG = None
        self.agent_id_list = []
        self.cache_manager = cache_manager
        # self.communication_manager = communication_manager
        self.loader_conn = loader_conn
        self.sub_task_agent_list = [] # that is the job list changed with job
        self.job_supervisor = None
    def _sub_task_agent_create(self,agent_id,job_description,return_content):
        sub_task_agent = SubTaskAgentContext(agent_id,job_description,return_content,self.cache_manager,
                                             "127.0.0.1",9956, self.loader_conn)
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




    def load_agent(self):
        """
        load the agent into the DAG
        Using topological sorting order for agent loading
        :return:
        """
    def generate_id(self):
        uni_id = str(time.time())[0:5]
        return uni_id
    def tasks_execute(self,response):
        #  1.1 获取依赖与子任务描述
        subTasks = response["sub_tasks"]
        dependencies = response["dependencies"]
        #  1.2 根据子任务创建智能体保存为列表
        id_list = [] # 记录id的映射关系列表
        sub_task_agents = [] # 记录创建的agent列表便于随机访问
        for item in subTasks:
            description = item["description"]
            return_content = item["return"]
            agentId = self.generate_id()
            id_list.append(agentId)
            sub_task_agent = self._sub_task_agent_create(agentId, description,return_content)
            sub_task_agents.append(sub_task_agent)
        #  2.1 根据依赖建立DAG图
        self.DAG = nx.DiGraph()
        # 2.1.1 初始化节点
        for i in range(len(sub_task_agents)):
            self.DAG.add_node(sub_task_agents[i])
        for k,v in dependencies.items():
            # 遍历该节点所需的依赖节点
            for node_raw_id in v:
                self.DAG.add_edge(sub_task_agents[int(k)-1],sub_task_agents[int(node_raw_id)-1])
        # 2.1.3 校验
        if nx.is_directed_acyclic_graph(self.DAG) is False:
            return error("DAG initialize fail")
        #  2.2 根据DAG图初始化JobSupervisor
        self.job_supervisor = JobSupervisor(self.DAG)
        #  3.1 执行DAG任务图并在JobSupervisor中进行同步记录
        self.job_supervisor.print_bitmap()
        agent_execute_list = self.topological_get_agent()
        for i in range(agent_execute_list):
            result = agent_execute_list[i].execute()
            # 智能体执行之后更新信息
            self.job_supervisor.update(result)
        #  3.2 将结果回传给Expert
        feed_back = self.job_supervisor.integer_task_execution_info()
        #  3.3 将输出结果传入task_schedule进行任务分析

        result = self.task_schedule(feed_back)


        return result
    def task_schedule(self,expert_feedback):
        # 当expert获得任务执行的反馈之后的操作
        pass

    def topological_get_agent(self):
        """
        使用拓扑排序获取任务的执行顺序
        :return: 返回一个列表，表示任务的执行顺序
        """
        # 初始化入度字典
        in_degree = defaultdict(int)
        for node in self.DAG.nodes():  # 使用 nodes() 方法获取所有节点
            in_degree[node] = 0

        # 计算每个节点的入度
        for node in self.DAG.nodes():  # 使用 nodes() 方法获取所有节点
            for neighbor in self.DAG.successors(node):  # 使用 successors() 方法获取邻居节点
                in_degree[neighbor] += 1

        # 初始化队列，将所有入度为 0 的节点加入队列
        queue = deque([node for node in in_degree if in_degree[node] == 0])

        # 拓扑排序结果
        topological_order = []

        # 拓扑排序
        while queue:
            current_node = queue.popleft()
            topological_order.append(current_node)
            # 遍历当前节点的依赖节点
            for neighbor in self.DAG.successors(current_node):  # 使用 successors() 方法获取邻居节点
                # 减少依赖节点的入度
                in_degree[neighbor] -= 1
                # 如果依赖节点的入度为 0，加入队列
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return topological_order

    def generate_id(self):
        uni_id = str(time.time())[0:5]
        return uni_id


