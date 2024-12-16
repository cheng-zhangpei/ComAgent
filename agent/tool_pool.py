import requests
from typing import Dict, List, Optional

class ToolPool:
    def __init__(self, tool_pool_ip: str, tool_pool_port: int):
        """
        初始化 ToolPool。
        :param tool_pool_ip: Tool Pool 的 IP 地址
        :param tool_pool_port: Tool Pool 的端口号
        """
        self.tool_pool_ip = tool_pool_ip
        self.tool_pool_port = tool_pool_port
        self.tool_server_info = None # list[dict]
        self.base_url = f"http://{self.tool_pool_ip}:{self.tool_pool_port}"


    def get_tool_servers(self) -> Dict:
        """
        获得工具服务器的大体信息，此处不需要往数据库里面找。
        :param tool_type: 工具类型（可选）
        :param tool_name: 工具名称（可选）
        :return: 工具列表
        """
        url = f"{self.base_url}/tool-server"

        response = requests.get(url)
        if response.status_code == 200:
            self.tool_server_info =  response.json()
            return self.tool_server_info
        else:
            raise Exception(f"Failed to get tools: {response.status_code}")

    def get_tools(
            self, tool_type: Optional[str] = None, tool_name: Optional[str] = None,tool_server: Optional[Dict] = None
    ) -> List[Dict]:
        """
        获取Tool Server工具列表。
        :param tool_server:
        :param tool_type: 工具类型（可选）
        :param tool_name: 工具名称（可选）
        :return: 工具列表
        """
        url = f"{self.base_url}/tools"
        params = {}
        if tool_type:
            params["tool_type"] = tool_type
        if tool_name:
            params["tool_name"] = tool_name
        if tool_server:
            params["tool_server"] = tool_server

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("tools", [])
        else:
            raise Exception(f"Failed to get tools: {response.status_code}")
    def execute_tool(self, tool_id: str, parameters: Dict) -> Dict:
        """
        执行指定工具。
        :param tool_id: 工具 ID
        :param parameters: 工具参数:这里的参数我估计都是String了估计，到时候类型还要小心一点，最好不要留到Tool Pool端解决
        :return: 执行结果
        """
        url = f"{self.base_url}/tools/{tool_id}/execute"
        payload = {"parameters": parameters}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to execute tool: {response.status_code}")

    def health_check(self) -> Dict:
        """
        检查 Tool Pool 的健康状态。
        :return: 健康状态信息
        """
        url = f"{self.base_url}/health"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to check health: {response.status_code}")