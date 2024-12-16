"""
@Function:             
@Author : ZhangPeiCheng
@Time : 2025/1/17 10:18
"""
import threading
import time

from sympy import false
from transformers.models.electra.modeling_electra import ElectraSelfAttention

from cache.comdb_client import ComDBClient


class CacheManager:
    def __init__(self,ip,port,threshold,endpoint,merge_interval,merge_data_file_thre):
        # 维护与comdb的链接
        self.client = ComDBClient(ip,port)
        # 记录agent与对话论数的映射(用于触发compress记忆压缩的操作)
        self.agent_to_epoch_com = {}
        # 至少需要多少条信息才可以出发压缩机制
        self.threshold = threshold
        # 压缩所需大模型endpoint
        self.endpoint = endpoint
        # 执行merge的间隔，单位是s
        self.merge_interval = merge_interval  # 默认 60 秒
        # 定时任务的线程
        self.merge_thread = None
        if self.test_conn():
            # 只要链接存在
            self.start_merge_task(merge_data_file_thre)

    def test_conn(self):
        if self.client.test_connection():
            return True
        return False
    #==================================================== memory operation ===========================================
    def MemPut(self,agent_id,value):
        err = self.client.memory_set(agent_id,value)
        if err:
            return False
        return True
    def MemGet(self,agent_id):
        result = self.client.get(agent_id)
        if result is None:
            print("无法获取记忆")
        return result
    def MemDelete(self,agent_id):
        if self.client.delete_memory_space(agent_id):
            return True
        return False
    def MemSearch(self,agent_id,search_content):
        search_result = self.client.memory_search(agent_id,search_content)
        if search_result is None:
            print("搜索失败")
        return search_result
    def Compress(self,agent_id):
        # 判断是否满足压缩条件
        if self.agent_to_epoch_com[agent_id] >= self.threshold:
            if self.client.compress_memory(agent_id,self.endpoint) is not None:
                return False
        else:
            return False

    def CompressAll (self):
        # 判断是否满足压缩条件
        can_compress_id = []
        for key,value in self.agent_to_epoch_com.items():
            if self.agent_to_epoch_com[key] >= self.threshold:
                can_compress_id.append(key)
        for agent_id in can_compress_id:
            if self.Compress(agent_id) is False:
                return False
        return True

    def CompressEpochRecord(self,agent_id):
        if  self.agent_to_epoch_com[agent_id] is None:
            self.agent_to_epoch_com[agent_id] = 1
        else:
            self.agent_to_epoch_com[agent_id] += 1
#=========================================================merge operation ===============================
    def merge_data(self):
        """
        执行 merge 操作的逻辑。
        """
        print("Running merge operation...")
        if self.client.merge() is True:
            print("merge successfully")
        else:
            print("merge failed")
    def start_merge_task(self,merge_data_file):
        """
        启动定时 merge 任务。
        :param interval: 用户指定的时间间隔（秒）
        """
        # 只需要一个后台的守护进程
        if self.merge_thread is not None:
            self.stop_merge_task()

        print(f"Starting merge task with interval: {self.merge_interval} seconds")
        # 定义定时任务的函数
        def run_merge_task():
            while True:
                # 获取数据库中的数据文件数量
                status = self.client.Stat()
                # 必须数据文件数量达到阈值之后才可以进行压缩
                if status["DataFile"] < merge_data_file:
                    time.sleep(self.merge_interval)
                self.merge_data()  # 执行 merge 操作
                time.sleep(self.merge_interval)
                # 启动后台线程
        self.merge_thread = threading.Thread(target=run_merge_task)
        self.merge_thread.daemon = True  # 设置为守护线程
        self.merge_thread.start()

    def stop_merge_task(self):
        """
        停止定时 merge 任务。
        """
        if self.merge_thread is not None:
            print("Stopping merge task...")
            # 通过设置标志位或终止线程来停止任务
            # 这里简单演示，实际中可以使用 threading.Event 来控制线程退出
            self.merge_thread.join(timeout=0)
            self.merge_thread = None



