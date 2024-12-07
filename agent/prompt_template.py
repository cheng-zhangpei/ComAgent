"""
@author        :ZhangPeiCheng
@function      :
@time          :2024/10/11 15:47
"""
import json
import re


def expert_agent_prompt(task, local_cache, global_cache):
    # 注：此处expert并不能获得工具池中的工具，现在的想法暂时是
    """

    :param task:任务描述
    :param local_cache:本地缓存
    :param global_cache:全局缓存
    :return:
    """
    prompt = f'''
你是一个专家智能体，你需要将一个复杂任务分解为多个子任务
你的任务是 "{task}"
历史信息:
{local_cache}
全局任务缓存:
{global_cache}
将你的协调信息按照下面的格式返回并对相应内容进行替换(只需要返回json部分的信息不能返回其他任何信息,并且只返回一次并在开头与结尾加上标记)：
<start_json>: json开始
<end_json>: json结束
下面是输出的模板，只需要输出下面json部分，上面是两个标记
{{
    "sub_tasks": [
        {{
            "id": 1,
            "description": "子任务描述",
            "return"："任务返回内容"
        }},
        {{
            "id": 2,
            "description": "子任务描述",
            "return"："任务返回内容"
                ...
        }}
        ...(根据任务弹性布置)
    ],
    # 下面这个是依赖图，也就是任务之间的同步关系。key为sub_tasks编号，后面的列表是任务的前置的条件
    "dependency_graph": {{
        "1": [],
        "2": [1]
        ...根据任务弹性布置
    }}
    "memory": {{
        此处添加记忆内容，内容为本次任务的核心流程等，尽可能简约
    }}
}}
不要包含输入内容的任何重复部分，只输出你的内容就好了，我输入的prompt不能附带在输出中，以上内容不能出现在输出中
    '''
    return prompt

def sub_task_agent_prompt(sub_task_description, link_cache, direct_agent_return, sub_task_id, tool_describe,return_info):
    prompt = f'''
你是一个子任务智能体服务于专家智能体的需求,你只需要输出下面输出格式中的内容
你的任务是:
"{sub_task_description}"
可用工具列表及其描述与参数信息:
"{tool_describe}"
你需要返回的信息是：
”{return_info}“
链路缓存（子任务可获得依赖路径上其他智能体的信息）
”{link_cache}“
直接相连智能体：
”{direct_agent_return}“
输出格式为：
{{
    "task_id": "{sub_task_id}", # 当前的智能体或者是任务id
    "status": "1/0", # 1代表任务完成，0代表任务异常
    "output": "任务的运行结果",
    ”analysis“: "任务的运行情况与对全局的分析"
}}

    '''
    return prompt


def llm_output_checkout(raw_data):
    try:
        match = re.search(r'```json([\s\S]*?)```', raw_data)
        if not match:
            raise ValueError("未找到有效的 JSON 数据")
        json_str = match.group(1).strip()
        json_data = json.loads(json_str)
        return json_data

    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return {"error": "Invalid JSON format"}
    except Exception as e:
        print(f"处理错误: {e}")
        return {"error": "Failed to extract JSON"}


def clean_and_parse(raw_data):
    # raw_data = raw_data[]
    matches = re.findall(r'<start_json>([\s\S]*?)<end_json>', raw_data)
    if len(matches) == 0:
        return 'error'
    for match in matches:
        try:
            cleaned_data = re.sub(r"<start_json>.*?\{", "{", match, flags=re.DOTALL)
            return json.loads(cleaned_data.strip())
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
        except Exception as e:
            print(f"JSON parse error: {e}")
    return 'error'


def extract_top_level(cleaned_data):
    """
    提取 JSON 数据中第一级的 sub_tasks 列表。
    """
    try:
        sub_tasks = cleaned_data.get("sub_tasks", [])
        if not sub_tasks:
            raise ValueError("未找到 sub_tasks 数据")
        # 打印提取出的第一级内容
        print("一级任务内容:")
        for task in sub_tasks:
            print(json.dumps(task, indent=4, ensure_ascii=False))
        return sub_tasks
    except Exception as e:
        print(f"提取第一级任务内容时出错: {e}")
        return []
