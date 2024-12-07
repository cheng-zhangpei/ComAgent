"""
@Function:1. 用于测试全局复杂情况下智能体运行效果，再逐渐迁移至云原生集群测试效果
          2. 后续逐渐替换etcd为自制的缓存kv数据库内核专用于agent数据缓存

@Author : ZhangPeiCheng
@Time : 2024/10/23 19:44
"""
import ast

from agent.AgentLoader import AgentLoader
from agent.prompt_template import expert_agent_prompt, extract_top_level
from cache.CacheManager import CacheManager
from communication.CommunicationManager import CommunicationManager
from communication.RabbitmqConnection import RabbitMQConnection
from session.ExpertSession import ExpertSession

import json
import re


model_name = r"D:\czp\k8s-mult-agent\resource\models\chengzipi\huggingface\Qwen-72B-2.5"
loader_ip = "127.0.0.1"
loader_port = "5000"
etcd_ip = "127.0.0.1"
etcd_port = 2379
rabbit_ip = "127.0.0.1"
rabbit_port = 5555




if __name__ == "__main__":
    # benchmark()
    message = ("我想要让你解决k8s的运维问题，你可以获取etcd中的集群信息，并根据用户的需求解决问题"
               "如果我让你可以调用k8s的api并且可以自动的创建子智能体，我现在想要在k8s"
               "中部署一个3个节点的mysql，主从节点由你自己搭配")
    expert_description = expert_agent_prompt(message,"ignore","ignore")

    agentLoader = AgentLoader(loader_ip,loader_port)
    # the loader here is the file path in server machine
    agentLoader.load_model(model_name) # create model in the remote machine or just use the schedule power of the k8s cluster
    # now the model should just run in the server
    # initialize the cacheManager
    cache_manager = CacheManager(etcd_ip,etcd_port)
    # the test will running on etcd ,orangeDB should be compatible with the demand here
    # initialize the communication
    # rabbitmq_conn = RabbitMQConnection()
    # communication_manager = CommunicationManager(rabbitmq_conn)
    session = ExpertSession(agentLoader,cache_manager,"",expert_description)
    session.session_boot()
    # start the assignment  and the session will just stay in the memory and never stop
    # the session will stop until we just give the exit command
##  session.session_boot()
