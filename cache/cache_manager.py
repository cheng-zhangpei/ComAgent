"""
@author        :ZhangPeiCheng
@function      :for managing the cache
@time          :2024/10/11 14:43
"""
import logging
import socket
from datetime import datetime

import etcd3
from etcd3 import Etcd3Client, client
from scipy.constants import value

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class CacheManager:
    """ manage the cache space
    We just run a CachedManger in one single session
    The user can not see the running of the cache manager
    """

    def __init__(self, etcd_ip, etcd_port):
        self.etcd_ip = etcd_ip
        self.etcd_port = etcd_port
        self.etcd_connection = client(host=self.etcd_ip, port=self.etcd_port)
        self.global_cache_path = "/agents/global"  # global cache path
        # 细化记忆空间

    def test_conn(self):
        try:
            with socket.create_connection((self.etcd_ip, self.etcd_port), timeout=5) as sock:
                logger.info(f"CacheManager Connection to {self.etcd_ip}:{self.etcd_port} is successful.")
                return True
        except socket.timeout:
            logger.info(f"CacheManager Connection to {self.etcd_ip}:{self.etcd_port} timed out.")
            return False
        except socket.error as e:
            logger.info(f"CacheManager Connection to {self.etcd_ip}:{self.etcd_port} failed: {e}")
            return False


    def write_task(self, key, value, agent_id):
        """
        we should set the format of the cache
        :param agent_id:
        :param value:
        :return:
        """
        cache_message = f'''
            "agent_id": {agent_id},
            "timestamp":"{datetime.now()}"
            "value":{str(value)}
        '''
        self.etcd_connection.put(key,cache_message)

    def get_memory(self, key):
        kv_value = self.etcd_connection.get(key)
        if kv_value[0] is not None:  # 检查值是否存在
            return kv_value[0].decode('utf-8')  # 将字节数组解码为字符串
        else:
            return None  # 如果值为空，返回 None


    def search_agent_cache(self):
        """"
        int this system:cache can deliver into 2 categories:
        1. self-memory:the memory will maintain in the local-cache-path(only expert agent)
        """
        # I hope I can add search functionality to the database.
        # I can just use the time/ some requirements to search the database
        # for agent, it can not just read his memory.should have an interesting mechanism to ensure the search process



        pass
    def get_by_prefix(self,prefix):
        # 使用 range 方法获取所有以 prefix 开头的键值对
        range_response = self.etcd_connection.get_prefix(prefix)

        # 解析结果并存储到字典中
        result = {}
        for kv in range_response:
            key = kv[1].key.decode('utf-8')  # 解码键
            value = kv[0].decode('utf-8')  # 解码值
            result[key] = value

        return result

    def delete_all_memory(self):
        key = self.local_cache_path
        return self.etcd_connection.delete_prefix(key)


    def write(self,key,value):
        """to initialize some value"""
        return self.etcd_connection.put(key,value)


    def delete(self,key):
        """to initialize some value"""
        return self.etcd_connection.delete(key)


    def read(self,key):
        kv_value = self.etcd_connection.get(key)
        return str(kv_value[0])[1:]


    def get_global_cache(self):
        """get global cache
        I just set the global cache key: /global
        """
        kv_value = self.etcd_connection.get(self.global_cache_path)
        return str(kv_value[0])[1:]


    def get_local_cache(self, agent_id):
        """
        get the cache of the agent
        :param agent_id:
        :return:
        """

        kv_value = self.etcd_connection.get(self.local_cache_path  + str(agent_id) )
        return str(kv_value[0])[1:]


if __name__ == "__main__":
    cacheManager = CacheManager("127.0.0.1",2379)
    cacheManager.test_conn()
