"""
@author        :ZhangPeiCheng
@function      :AgentLoader：load agent into the session
@time          :2024/9/26 20:56
"""
from llama_cpp import Llama


class AgentLoader:
    def __init__(self, model_path):
        self.model_path = model_path

    def load(self):
        llm = Llama(
            model_path=self.model_path,
            # n_gpu_layers=-1, # Uncomment to use GPU acceleration
            # seed=1337, # Uncomment to set a specific seed
            # n_ctx=2048, # Uncomment to increase the context window
        )
