"""
@author        :ZhangPeiCheng
@function      :
@time          :2024/10/11 15:47
"""


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
将你的协调信息按照下面的格式返回：
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
}}
    '''
    return prompt


def sub_task_agent_prompt(sub_task_description, link_cache, direct_agent_return, sub_task_id, tool_describe,return_info):
    prompt = f'''
你是一个子任务智能体服务于专家智能体的需求
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
