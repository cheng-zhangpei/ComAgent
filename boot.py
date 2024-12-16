"""
@Function:1. 用于测试全局复杂情况下智能体运行效果，再逐渐迁移至云原生集群测试效果
          2. 后续逐渐替换etcd为自制的缓存kv数据库内核专用于agent数据缓存

@Author : ZhangPeiCheng
@Time : 2024/10/23 19:44
"""
import ast
import json

from agent.agent_loader import AgentLoader
from agent.tool_pool import ToolPool
from agent.prompt_template import initial_prompt_expert
from cache.cache_manager import CacheManager
from session.ExpertSession import ExpertSession

# 让用户通过配置文件导入内容
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    message = ("我想要让你解决k8s的运维问题，你可以获取etcd中的集群信息，并根据用户/工程师的需求解决问题")
    file_path = "./config/config.json"  # 假设 JSON 文件名为 config.json
    config_data = read_json_file(file_path)
    model_name = config_data["model_name"]
    loader_ip = config_data["loader_ip"]
    loader_port = config_data["loader_port"]
    etcd_ip = config_data["etcd_ip"]
    etcd_port = config_data["etcd_port"]
    tool_pool_host = config_data["tool_pool_host"]
    tool_pool_port = config_data["tool_pool_port"]

    expert_description = initial_prompt_expert(message)
    agentLoader = AgentLoader(loader_ip,loader_port)
    # the loader here is the file path in server machine
    # agentLoader.load_model(model_name) # create model in the remote machine or just use the schedule power of the k8s cluster
    # now the model should just run in the server
    cache_manager = CacheManager(etcd_ip,etcd_port)
    tool_pool = ToolPool(tool_pool_host,tool_pool_port)
    session = ExpertSession(agentLoader,cache_manager,message,expert_description)
    session.session_boot()
