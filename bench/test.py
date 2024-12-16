"""
@Function:             
@Author : ZhangPeiCheng
@Time : 2024/12/13 16:25
"""
from etcd3 import client

from cache.cache_manager import CacheManager
# 用于清除显卡显存
import torch

torch.cuda.empty_cache()