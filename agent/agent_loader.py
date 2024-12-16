"""
@author        :ZhangPeiCheng
@function      :AgentLoader：load agent into the session
@time          :2024/9/26 20:56
"""
import logging
import os
import socket
import time

import requests
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from agent.prompt_template import initial_prompt_expert

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class AgentLoader:
    """
    message format:

    """
    def __init__(self,ip, port, message = "", load_method = "int4",job="expert"):
        self.ip = ip
        self.port  = port
        self.job = job # use to  identify
        self.load_method = load_method # loading method
        self.message = message

    def test_conn(self):
        try:
            with socket.create_connection((self.ip, self.port), timeout=5) as sock:
                logger.info(f"AgentLoader Connection to {self.ip}:{self.port} is successful.")
                return True
        except socket.timeout:
            logger.info(f"AgentLoader Connection to {self.ip}:{self.port} timed out.")
            return False
        except socket.error as e:
            logger.info(f"AgentLoader Connection to {self.ip}:{self.port} failed: {e}")
            return False

    def load_model(self,model_path):

        # build the request about loading model into the memory
        url = f"http://{self.ip}:{self.port}/load_model_local"
        payload = {"model_path": model_path}
        try:
            logger.info("the model is loading in the server")
            response = requests.post(url, json=payload)
            logger.info("the model is loaded in the server")
            return response.json()
        except  Exception as e:
            logger.error(f"预测请求失败: {e}")


    def send_message(self,message,max_value=1024):
        # send the message about the operation,the message here will be compounded with the context in agent runtime
        url = f"http://{self.ip}:{self.port}/generate"
        payload = {"message": message,"max_value": max_value}
        try:
            logger.info("the model is working")
            response = requests.post(url, json=payload)
            response = response.json()
            return response['result']
        except  Exception as e:
            logger.error(f"预测请求失败: {e}")

#
# model_name = r"D:\czp\k8s-mult-agent\resource\models\chengzipi\huggingface\Qwen-72B-2.5"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto",  quantization_config=bnb_config).eval()
# message = ("我想要让你解决k8s的运维问题，你可以获取etcd中的集群信息，并根据用户的需求解决问题，你对k8s的了解如何，"
#            "如果我让你可以调用k8s的api并且可以自动的创建子智能体，你是否有信心解决复杂的运维问题？,比如我现在想要在k8s中部署一个3个节点的mysql你给我详细的步骤看看")
# mess = initial_prompt_expert(message,"ignore","ignore")
# inputs = tokenizer(mess, return_tensors='pt')
# inputs = inputs.to(model.device)
# generated_ids = model.generate(
#     **inputs,
#     max_new_tokens=1024,  # 限制生成的新 token 长度
#     do_sample=True,  # 是否启用采样，提升生成的多样性
#     temperature=0.7,  # 控制输出的随机性
#     top_p=0.9,  # nucleus sampling
#     use_cache=True,  # 启用缓存以加速生成
# )
#
# # 实时解码输出
# for i, token_id in enumerate(generated_ids[0]):
#     token = tokenizer.decode(token_id, skip_special_tokens=True)
#     print(token, end="", flush=True)  # 实时输出
# print("装入模型...")
# pred = model.generate(**inputs,max_length=5000)
#
# print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))
