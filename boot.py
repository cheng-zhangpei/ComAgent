"""
@Function:1. 用于测试全局复杂情况下智能体运行效果，再逐渐迁移至云原生集群测试效果
          2. 后续逐渐替换etcd为自制的缓存kv数据库内核专用于agent数据缓存

@Author : ZhangPeiCheng
@Time : 2024/10/23 19:44
"""
from agent.AgentLoader import AgentLoader
from session.ExpertSession import ExpertSession
model_name = r"D:\czp\k8s-mult-agent\resource\models\chengzipi\huggingface\Qwen-72B-2.5"
loader_ip = "127.0.0.1"
loader_port = "5000"

if __name__ == "__main__":
    # benchmark()
    agentLoader = AgentLoader(loader_ip,loader_port)
    # the loader here is the file path in server machine
    agentLoader.load_model(model_name) # create model in the remote machine or just use the schedule power of the k8s cluster

    # session = ExpertSession()
    # pass
