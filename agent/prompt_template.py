"""
@author        :ZhangPeiCheng
@function      :
@time          :2024/10/11 15:47
"""


def expert_agent_prompt(task, local_cache, global_cache, tool_config_list):
    prompt = f'''
You are an Expert Agent responsible for decomposing a task into sub-tasks. 
The conversation has a local cache and a global cache to assist you. Use the data from the cache when necessary.

Here is the task: "{task}"

Local Cache:
{local_cache}

Global Cache:
{global_cache}

tool_description_list:
{tool_config_list}
Please divide the task into several sub-tasks, and structure the result as follows(response format):
{{
    "task": "{task}",
    "sub_tasks": [
        {{
            "id": 1,
            "description": "Sub-task 1 description",
            "dependencies": [],  # Dependencies: list of sub-task ids this task depends on
            "local_cache_used": ["cache_key_1"],  # Local cache entries used
            "global_cache_used": ["cache_key_2"],  # Global cache entries used
            "tool_address": tool_ip:port + path,
            "parameters": {{
                "param_1": "value_1",
                "param_2": "value_2"
                ...
            }}
        }},
        {{
            "id": 2,
            "description": "Sub-task 2 description",
            "dependencies": [1],  # Depends on sub-task 1
            "local_cache_used": [],
            "global_cache_used": ["cache_key_3"],
            "tools": ["Tool_C"],
            "tool_address": tool_ip:port + path,
                "param_1": "value_1",
                "param_2": "value_2"
                ...
            }}
        }}...(schedule with the task change)
    ],
    "dependency_graph": {{
        "1": [],
        "2": [1]
    }}
}}

Return the task decomposition in the above format. Ensure all sub-tasks include the correct dependencies, 
the tools required, and the parameters needed for execution. Also, clearly indicate which cache entries 
(both local and global) were used to assist in the task breakdown.
    '''
    return prompt


def sub_task_agent_prompt(sub_task_description, dependencies, local_cache, global_cache, sub_task_id, tool_path):
    prompt = f'''
You are a Sub-Task Agent responsible for executing a specific sub-task in a distributed system.

Here is your task:
"{sub_task_description}"
The tool you should use:
"{tool_path}"
You must consider the following:
- Dependencies: This task depends on the completion of the following tasks: {dependencies}. Ensure all dependencies are completed before starting.
- Local Cache: Here is the local cache available for this task: {local_cache}. Use this cache to optimize the task execution.
- Global Cache: The following data is available from the global cache: {global_cache}. If needed, use this data to assist in the task execution.

Please execute the task according to the given parameters and report back when completed.
Return the results in the following format:
{{
    "task_id": "{sub_task_id}",
    "status": "completed",
    "output": "Execution details or results here",
    "local_cache_used": ["list_of_used_local_cache_keys"],
    "global_cache_used": ["list_of_used_global_cache_keys"]
}}
    '''
    return prompt
