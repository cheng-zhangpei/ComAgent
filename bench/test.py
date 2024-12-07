"""
@Function:             
@Author : ZhangPeiCheng
@Time : 2024/12/13 16:25
"""
from etcd3 import client

from cache.CacheManager import CacheManager

etcd_connection = client(host="127.0.0.1", port=2379)
print(etcd_connection.get_all_response())