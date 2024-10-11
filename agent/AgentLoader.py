"""
@author        :ZhangPeiCheng
@function      :AgentLoader：load agent into the session
@time          :2024/9/26 20:56
"""
from agent.AgentTemplate import BaseAgent

# 这个类后面可以尝试修改成模型池，可以提供弹性化的模型优化管理策略
class ModelLoader:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = self.load_model()
    def load_model(self):
        # 将model load 到 memory/ gpu中
        return AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="auto"
    )


class AgentLoader:
    """该类用于装载专家模型或者是子智能体"""
    def __init__(self,model_name,characteristic = "expert"):
        self.characteristic = characteristic
        self.model_name  = model_name
        self.model = self.load_model()

    def load_model(self):
        # 将model load 到 memory/ gpu中
        return AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="auto"
        )

    def expert_load(self):
        # 这个的函数是在Session中率先创建的
        pass
    def sub_class_load(self):
        # 这个函数是在decomposer中工具expert的输出进行sub-class的创建
        pass






from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "Qwen/Qwen2.5-72B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
