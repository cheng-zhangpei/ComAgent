"""
@Function:             
@Author : ZhangPeiCheng
@Time : 2024/12/16 08:59
"""
from collections import deque, defaultdict

import networkx as nx
class JobSupervisor:
    def __init__(self, DAG):
        self.DAG = DAG  # DAG 是一个字典，表示任务依赖关系
        self.bitmap = {}  # 初始化 bitmap
        self.create_bit_map()  # 创建 bitmap

    from collections import defaultdict, deque

    def create_bit_map(self):
        """
        使用手动实现的拓扑排序遍历 DAG，构建 bitmap
        """
        # 初始化入度字典
        in_degree = defaultdict(int)
        for node in self.DAG.nodes():
            in_degree[node] = 0

        # 计算每个节点的入度
        for node in self.DAG.nodes():
            for neighbor in self.DAG.successors(node):
                in_degree[neighbor] += 1

        # 初始化队列，将所有入度为 0 的节点加入队列
        queue = deque([node for node in in_degree if in_degree[node] == 0])
        # 拓扑排序
        while queue:
            current_node = queue.popleft()
            # 初始化当前节点的 bitmap 条目
            self.bitmap[current_node] = {}
            # 遍历当前节点的依赖节点
            for neighbor in self.DAG.successors(current_node):
                # 将依赖节点添加到当前节点的 bitmap 中，状态初始化为 0
                self.bitmap[current_node][neighbor] = 0
                # 减少依赖节点的入度
                in_degree[neighbor] -= 1
                # 如果依赖节点的入度为 0，加入队列
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    def get_bitmap(self):
        """
        返回构建的 bitmap -> 模型的运行的顺序就依靠bitmap
        """
        return self.bitmap

    def print_bitmap(self):
        """
        打印 bitmap，显示每个节点及其依赖节点的状态
        """
        print("BitMap Representation:")
        for node, dependencies in self.bitmap.items():
            print(f"Node: {node}")
            if dependencies:
                for neighbor, status in dependencies.items():
                    print(f"  -> Depends on Node: {neighbor}, Status: {status}")
            else:
                print("  -> No dependencies")
            print("-" * 40)

    def integer_task_execution_info(self):
        pass

    def update(self, result):
        # 用于更新bitmap以及任务状态信息
        pass
if __name__ == "__main__":
    DAG = {
        "task1": ["task2", "task3"],
        "task2": ["task4"],
        "task3": ["task4"],
        "task4": []
    }

    # 使用 TaskManager
    task_manager = JobSupervisor(DAG)
    bitmap = task_manager.get_bitmap()
    # 输出 bitmap
    print("Bitmap:", bitmap)