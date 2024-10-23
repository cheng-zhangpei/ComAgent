"""
@author        :ZhangPeiCheng
@function      :for managing the cache
@time          :2024/10/11 14:43
"""
from datetime import datetime

import etcd


class CacheManager:
    """ manage the cache space
    We just run a CachedManger in one single session
    The user can not see the running of the cache manager
    """

    def __init__(self, etcd_ip, etcd_port):
        self.etcd_ip = etcd_ip
        self.etcd_port = etcd_port
        # single instance initialization
        self.etcd_connection = etcd.Client(host=self.etcd_ip, port=self.etcd_port)
        self.global_cache_path = "/agents/global"  # global cache path
        self.local_cache_path = f"/agents/"  # local cache path

    def write_agent_cache(self, value, agent_id):
        """
        we should set the format of the cache
        这个方法针对
        :param agent_id:
        :param value:
        :return:
        """
        key = self.local_cache_path+agent_id
        # 封装消息格式
        cache_message = f'''
            "agent_id": {agent_id},
            "timestamp":"{datetime.now()}"
            "value":{value}
        '''
        self.etcd_connection.write(key,cache_message)
    def write(self,key,value):
        self.etcd_connection.write(key,value)
    def get_global_cache(self):
        """get global cache
        I just set the global cache key: /global
        """
        pass

    def get_local_cache(self, agent_id):
        """
        get the cache of the agent
        :param agent_id:
        :return:
        """
        pass

    def get_link_cache(self, link_id):
        """
        get the link cache
        :param link_id:
        :return:
        """

    def cut_memory_space(self):
        """

        :return:
        """
