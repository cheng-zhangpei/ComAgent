"""
@Function:             
@Author : ZhangPeiCheng
@Time : 2025/1/16 11:44
"""
import requests


# 这个其实都可以直接取代之前的CacheManager的功能了，因为直接在数据库层维护记忆空间了

class ComDBClient:
    def __init__(self, ip="localhost", port=9090):
        """
        Initialize the ComDBClient instance.

        :param ip: The IP address of the ComDB server.
        :param port: The port number of the ComDB server.
        """
        self.addr = f"http://{ip}:{port}"

    def test_connection(self):
        """
        Test the connection to the ComDB server.

        :return: True if the connection is successful, False otherwise.
        """
        try:
            response = requests.get(f"{self.addr}/health")
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Connection test failed: {e}")
            return False

    def get(self, key):
        """
        Retrieve the value for a given key from the ComDB server.

        :param key: The key to retrieve.
        :return: The value associated with the key, or None if not found.
        """
        try:
            response = requests.get(f"{self.addr}/bitcask/get", params={"key": key})
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to get key '{key}': {response.status_code} {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Error during GET request: {e}")
            return None

    def put(self, key, value):
        """
        Store a key-value pair in the ComDB server.

        :param key: The key to store.
        :param value: The value to store.
        :return: True if the operation is successful, False otherwise.
        """
        try:
            # 构造符合服务器端期望的请求体
            data = {key: value}
            # 发送POST请求
            response = requests.post(f"{self.addr}/bitcask/put", json=data)

            # 检查响应状态码
            if response.status_code == 200:
                return True
            else:
                print(f"Failed to put key '{key}': {response.status_code} {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Error during PUT request: {e}")
            return False

    def listKey(self):
        """
        List all key stored in the comDB server
        :return: True if the operation is successful, False otherwise.
        """
        try:
            response = requests.get(f"{self.addr}/bitcask/listkeys")
            if response.status_code == 200:
                return response.text
            else:
                print( response.status_code)
                print("Failed to list keys")
                return False
        except requests.RequestException as e:
            print(f"Error during listkeys request: {e}")
            return False

    def Stat(self):
        """
        get the status of the ComDB server
        :return: True if the operation is successful, False otherwise.
        """
        try:
            response = requests.get(f"{self.addr}/bitcask/stat")
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to state the database")
                return False
        except requests.RequestException as e:
            print(f"Error during stat request: {e}")
            return False

    def delete(self, key):
        """
        delete data
        :param key:  key。
        """
        try:
            response = requests.delete(f"{self.addr}/bitcask/delete", params={"key": key})
            if response.status_code == 200:
                print(f"Key '{key}' deleted successfully.")
                return True
            else:
                print(f"Failed to delete key '{key}': {response.status_code} {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Error during DELETE request: {e}")
            return False
    def get_by_prefix(self, prefix):
        """
          Retrieve the value for a given key from the ComDB server.

          :param prefix: The prefix of the key
          :return: The value associated with the key, or None if not found.
      """
        try:
            response = requests.get(f"{self.addr}/bitcask/prefix", params={"prefix": prefix})
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to get prefix '{prefix}': {response.status_code} {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Error during PREFIX request: {e}")
            return None
    def memory_get(self,agentId):
        """
        Gain all the memory of the agentId
        notice: if you set the memorySize with a large number. it may cause some unpredictable err.
        :param agentId: the unique label of the agent in the database,you can manage the memory space by agentId
        :return: The value associated with the key, or None if not found.
        """
        try:
            response = requests.get(f"{self.addr}/memory/get", params={"agentId": agentId})
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to get memory from agentId:'{agentId}': {response.status_code} {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Error during MEMORY/GET request: {e}")
            return None

    def memory_set(self, agent_id, value):
        """
        set memory

        :param agent_id: agent unique label。
        :param value: value。
        """
        try:
            data = {
                "agentId": agent_id,
                "value": value
            }

            response = requests.post(f"{self.addr}/memory/set", json=data)

            if response.status_code == 200:
                print(f"Value stored successfully for agent '{agent_id}'.")
                return True
            else:
                print(f"Failed to store value for agent '{agent_id}': {response.status_code} {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Error during memory set request: {e}")
            return False

    def memory_search(self, agent_id, search_item):
        """
        Search the memory space of the specified agent for the given search item.

        :param agent_id: The unique identifier of the agent.
        :param search_item: The search query to match against the agent's memory.
        :return: The search results if successful, otherwise None.
        """
        try:
            # Send a GET request to the /memory/search endpoint
            response = requests.get(
                f"{self.addr}/memory/search",
                params={"agentId": agent_id, "searchItem": search_item}
            )

            # Check the response status code
            if response.status_code == 200:
                # Parse and return the search results
                return response.json()
            else:
                print(f"Failed to search memory for agent '{agent_id}': {response.status_code} {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Error during memory search request: {e}")
            return None

    def create_memory_meta(self, agent_id, total_size):
        """
        Create a new memory space for the specified agent.

        :param agent_id: The unique identifier of the agent.
        :param total_size: The total size of the memory space to create.
        :return: The created memory metadata if successful, otherwise None.
        """
        try:
            # Construct the request body
            data = {
                "agentId": agent_id,
                "totalSize": total_size
            }

            # Send a POST request to the /memory/create endpoint
            response = requests.post(f"{self.addr}/memory/create", json=data)

            # Check the response status code
            if response.status_code == 200:
                # Parse and return the created memory metadata
                return response.json()
            else:
                print(f"Failed to create memory space for agent '{agent_id}': {response.status_code} {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Error during memory creation request: {e}")
            return None

    def compress_memory(self, agent_id, endpoint):
        """
        Compress the memory space of the specified agent using the provided compression endpoint.

        :param agent_id: The unique identifier of the agent.
        :param endpoint: The compression endpoint to use for compressing the memory.
        :return: True if the compression was successful, otherwise False.
        """
        try:
            # Construct the request body
            data = {
                "agentId": agent_id,
                "endpoint": endpoint
            }

            # Send a POST request to the /memory/compress endpoint
            response = requests.post(f"{self.addr}/memory/compress", json=data)

            # Check the response status code
            if response.status_code == 200:
                # Parse the response to check if compression was successful
                result = response.json()
                if result.get("success", False):
                    print(f"Memory compression successful for agent '{agent_id}'.")
                    return True
                else:
                    print(f"Memory compression failed for agent '{agent_id}'.")
                    return False
            else:
                print(f"Failed to compress memory for agent '{agent_id}': {response.status_code} {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Error during memory compression request: {e}")
            return False

    def create_compressor(self, agent_id, endpoint):
        """
        Create a compressor for the specified agent's memory space.

        :param agent_id: The unique identifier of the agent.
        :param endpoint: The compression endpoint to use for the compressor.
        :return: True if the compressor was created successfully, otherwise False.
        """
        try:
            # Construct the request body
            data = {
                "agentId": agent_id,
                "endpoint": endpoint
            }

            # Send a POST request to the /memory/create-compressor endpoint
            response = requests.post(f"{self.addr}/memory/create-compressor", json=data)

            # Check the response status code
            if response.status_code == 200:
                print(f"Compressor created successfully for agent '{agent_id}'.")
                return True
            else:
                print(f"Failed to create compressor for agent '{agent_id}': {response.status_code} {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Error during compressor creation request: {e}")
            return False
    def delete_memory_space(self, agent_id):
        """
        Create a compressor for the specified agent's memory space.

        :param agent_id: The unique identifier of the agent.
        :param endpoint: The compression endpoint to use for the compressor.
        :return: True if the compressor was created successfully, otherwise False.
        """
        try:
            # Construct the request body
            data = {
                "agentId": agent_id,
            }
            # Send a POST request to the /memory/create-compressor endpoint
            response = requests.post(f"{self.addr}/memory/delete", json=data)

            # Check the response status code
            if response.status_code == 200:
                print(f"memory deleted successfully for agent '{agent_id}'.")
                return True
            else:
                print(f"Failed to delete memory for agent '{agent_id}': {response.status_code} {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Error during delete memory request: {e}")
            return False
    def merge(self):
        """
        merge the data in the database
        :return: True if the compressor was created successfully, otherwise False.
        """
        try:
            response = requests.post(f"{self.addr}/bitcask/merge", )
            if response.status_code == 200:
                print(f"the data have been merged successfully.")
                return True
            else:
                print(f"Failed to merge")
                return False
        except requests.RequestException as e:
            print(f"Failed to merge")
            return False