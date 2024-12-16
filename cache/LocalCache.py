"""
@Function:  用于框架的模型缓存
@Author : ZhangPeiCheng
@Time : 2024/12/30 19:50
"""
json_str = '''
{
    "sub_tasks": [
        {
            "id": 1,
            "description": "创建 MySQL 的 Kubernetes Namespace",
            "return": "Namespace 'mysql-cluster' 创建成功"
        },
        {
            "id": 2,
            "description": "创建 MySQL 的 PersistentVolume (PV) 和 PersistentVolumeClaim (PVC)",
            "return": "PV 和 PVC 创建成功，存储已分配"
        },
        {
            "id": 3,
            "description": "部署 MySQL StatefulSet，配置 3 个节点",
            "return": "MySQL StatefulSet 部署成功，3 个 Pod 正在运行"
        },
        {
            "id": 4,
            "description": "创建 MySQL 的 Service，提供集群访问",
            "return": "Service 'mysql-service' 创建成功，集群可访问"
        },
        {
            "id": 5,
            "description": "配置 MySQL 主从复制和集群高可用",
            "return": "MySQL 主从复制配置完成，集群高可用已启用"
        }
    ],
    "dependencies": {
        "1": [],
        "2": ["1"],
        "3": ["2"],
        "4": ["3"],
        "5": ["3"]
    },
    "memory": {
        "task_description": "在 Kubernetes 上部署一个高可用的 MySQL 集群，包含 3 个节点",
        "config": {
            "namespace": "mysql-cluster",
            "storage_class": "standard",
            "storage_size": "10Gi",
            "mysql_image": "mysql:8.0",
            "replicas": 3
        },
        "tools": [
            "kubectl",
            "Helm (可选)",
            "MySQL 配置工具"
        ]
    }
}
'''