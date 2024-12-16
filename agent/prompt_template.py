"""
@author        :ZhangPeiCheng
@function      :
@time          :2024/10/11 15:47
"""
import json
import re


def initial_prompt_expert(task):
    """

    :param task:任务描述
    :param local_cache:本地缓存
    :param global_cache:全局缓存
    :return:
    """
    prompt = f'''
你是一个专家智能体，你需要将一个复杂任务分解为多个子任务
这条信息是一个起始信息,用户会传入一个需要你完成任务的大致描述,你需要根据用户描述进行相应的欢迎
这条信息返回之后,服务器会为你建议记忆空间后续数据的发送就会包括
你的任务是 "{task}",
    '''
    return prompt

def expert_task_prompt(memory,task_description,config):
    prompt = f'''
    下面是我给你当前任务执行信息
    任务描述:{task_description}
    记忆信息{memory}  # 由任务所决定的所需记忆内容在后台查找后会添加到这个位置
    配置:{config} # 一些必要的配置信息以复制决策
    # todo: 添加任务服务器的任务配置，给与任务服务器中所提供的大致工具信息辅助决策
    下面是你的回答，请使用json格式进行回答，并使用<start_json>与<end_json>将生成的内容包裹方便解析
    如(一定要严格按照下面的格式否则会出错)：
    <start_json>
    {{
        sub_tasks:[
            {{
                id:1,
                description:"子任务描述"
                return: "任务返回内容"
            }},
            {{
                id:2,
                description:"子任务描述"
                return: "任务返回内容"
            }},
            ...  
        ],
        "dependencies":{{
            "1":[],
            "2":["1"],
        ...
        }},
        memory:{{
            此处添加简易的记忆内容如当前任务信息等内容
        }}
    }}
    <end_json>
        '''
    return prompt

def expert_task_schedule(status,memory,config,fail_info = ""):
    prompt = f'''
    下面是我给你当前任务执行信息
    任务执行状态：{status} #"1":任务成功 "0":任务失败
    失败智能体状态：{fail_info} # 会详细记录任务智能体的失败状态 
    记忆信息{memory}  # 由任务所决定的所需记忆内容在后台查找后会添加到这个位置
    配置:{config} # 一些必要的配置信息以复制决策
    # todo: 添加任务服务器的任务配置，给与任务服务器中所提供的大致工具信息辅助决策
    下面是你的回答，请使用json格式进行回答，并使用<start_json>与<end_json>将生成的内容包裹方便解析
    子任务划分的标准是该任务是否可以通过一个配置文件或者是一个api调用可以解决。
    如在k8s中一些较为复杂的操作直接可以在一个yaml文件中完成不需要划分为多个任务，子智能体只需要生成文件并部署即可
    如：
    <start_json>
    {{
         status:1/0, # 请回答0或者1，如果是1，后面的字段全部无效。只有为0才需要生成后面的字段
         restart:1/0, # 如果是1就会重新读取任务的描述重新生成任务链路，该任务链路需要避免之前任务执行的错误，如果是0
         modified_tasks:{{ # 该字段是读取异常之后重新调整的任务
             sub_tasks:[
                {{
                    id:1,
                    description:"子任务描述"
                    return: "任务返回内容"
                }},
                {{
                    id:2,
                    description:"子任务描述"
                    return: "任务返回内容"
                }},
                ...  
            ],
            "dependencies":{{ # 任务之间的依赖关系
                "1":[],
                "2":["1"],
            ...
            }},
            memory:{{
                此处添加简易的记忆内容如当前任务信息等内容
            }}
        }}
                
     }}
    <end_json>
'''
    return prompt


def expert_memory_search(tasks_description,info):
    prompt = f'''
    你自己选择该任务需要读取哪些部分记忆信息
    任务内容:{tasks_description}
    附加信息:{info}
    下面是你的回答，需要你按照下面的格式进行决策，请使用json格式进行回答，并使用<start_json>与<end_json>将生成的内容包裹方便解析
    如：
    <start_json>
    {{
        "task_key_word":["关键字1"，"关键字2",.....], # 用于搜索任务描述历史记忆空间
        "output_key_word":["关键字1"，"关键字2",.....], # 用于搜索决策历史历史空间
        "jobs_key_word":["关键字1"，"关键字2",.....], # 用于搜索任务执行情况历史空间
        ... #后续会添加更多的搜索方式，看数据库层所提供的搜索接口，暂时设置为需要同时对三个空间进行搜索
    }}
'''
    return prompt


def sub_task_agent_server_prompt(tool_server_info,sub_task_description,return_content):
    # sub-task agent获取Tool server信息
    prompt = f'''
你是一个子任务智能体服务于专家智能体的需求,你只需要输出下面输出格式中的内容
下面是不同服务器所提供的工具类型的数据：
"{tool_server_info}"
你的任务是:
"{sub_task_description}"
你最终返回给下一个智能体的数据是：
”{return_content}“
下面给出你的初步决策，每一步的决策尽可能简单,仅可以使用单一Tool完成
决策输出格式为(注意其余的信息都不要进行生成)：
<start_json>
{{
 	"jobs":[
 	"0":{{
 		"func_describe":"此处描述需要用的工具",
 		"server_id": "根据server信息给出工具会属于的server",
	}},
	"1":{{
 		"func_describe":"此处描述需要用的工具",
 		"server_id": "根据server信息给出工具会属于的server",
	}}, # ....根据自己需要添加 
    ]
}}
<end_json>
 '''
    return prompt

def sub_task_agent_tools_prompt(server_id,tools_info,job_description):
    # sub-task agent获取服务器上的Tool信息
    prompt = f'''
    你是一个子任务智能体服务于专家智能体的需求,你只需要输出下面输出格式中的内容
    下面是{server_id}服务器所提供的工具详细数据的数据：
    "{tools_info}"
    你的任务是:
    "{job_description}"
    下面给出你的初步决策，每一步的决策尽可能简单,仅可以使用单一Tool完成
    决策输出格式为(注意其余的信息都不要进行生成,xxx是你需要填充的内容，你只允许调用一个工具)：
    <start_json>
    {{
     	tool_id:"xxx"
     	tool_name:"xxx"
     	tool_parameter:[
     	    parameter1: "xxx" 
     	    parameter2: "xxx"
     	    ... 
     	]
    }}
    <end_json>
    若Tool 无法满足需求则返回
    <start_json>
    {{
     	error: "tool can not satisfy the requirement"
    }}
    <end_json>
     '''
    return prompt


def sub_task_agent_response_prompt(execute_status,return_content):
    # sub-task agent获取服务器上的Tool信息
    prompt = f'''
        你是一个子任务智能体服务于专家智能体的需求,你只需要输出下面输出格式中的内容
        你需要对前面链路的工具调用情况进行汇总
        你的需要汇总的数据有:
        "{execute_status}"
        你需要向下一个智能体传递的内容：
        "{return_content}"
        决策输出格式为(注意其余的信息都不要进行生成,xxx是你需要填充的内容)：
        <start_json>
        {{
            "execute_status": "success/error(decided by the execution info)",
            "return_content": {{
                "content1": xxx,
                "content2": xxx,
                // 可以根据需要继续添加更多内容
            }}
        }}
        <end_json>
        若需要重新规划任务
        <start_json>
        {{
         	error:"restart"
        }}
        <end_json>
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


def json_encode(raw_data):
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
