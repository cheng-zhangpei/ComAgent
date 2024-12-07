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
        # single instance initialization
        self.etcd_connection = client(host=self.etcd_ip, port=self.etcd_port)
        self.global_cache_path = "/agents/global"  # global cache path
        self.local_cache_path = "/agents/"  # local cache path


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


    def write_agent_cache(self, value, agent_id):
        """
        we should set the format of the cache
        :param agent_id:
        :param value:
        :return:
        """
        key = self.local_cache_path + agent_id + "/" + str(datetime.now())


        cache_message = f'''
            "agent_id": {agent_id},
            "timestamp":"{datetime.now()}"
            "value":{value}
        '''
        self.etcd_connection.put(key,cache_message)



    def search_agent_cache(self):
        """"
        int this system:cache can deliver into 2 categories:
        1. self-memory:the memory will maintain in the local-cache-path(only expert agent)
        """
        # I hope I can add search functionality to the database.
        # I can just use the time/ some requirements to search the database
        # for agent, it can not just read his memory.should have an interesting mechanism to ensure the search process



        pass





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
class MyCacheManager:
    """

    """
    pass

if __name__ == "__main__":
    cacheManager = CacheManager("127.0.0.1",2379)
    cacheManager.test_conn()
