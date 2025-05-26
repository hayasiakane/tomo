from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
import uuid
from datetime import datetime
from gremlin_python.process.graph_traversal import __

# class GremlinDB:
#     def __init__(self, endpoint=None):
#         self.endpoint = endpoint or "ws://localhost:8182/gremlin"
#         self.graph = Graph()
#         self.connection = None
#         self.g = None
        
#     def init_app(self, app):
#         self.endpoint = app.config.get('GREMLIN_SERVER_URL', self.endpoint)
#         self.connect()
        
#     def connect(self):
#         self.connection = DriverRemoteConnection(self.endpoint, 'g')
#         self.g = self.graph.traversal().withRemote(self.connection)
        
#     def close(self):
#         if self.connection:
#             self.connection.close()
# # 全局数据库实例
# db = GremlinDB()

class GremlinDB:
    def __init__(self, endpoint=None):
        self._connection = None
        self._g = None
        self.endpoint = endpoint or "ws://localhost:8182/gremlin"
        
    def init_app(self, app):
        """Flask应用初始化"""
        self.endpoint = app.config.get('GREMLIN_SERVER_URL', self.endpoint)
        
    @property
    def g(self):
        """获取图遍历器（延迟初始化）"""
        if not self._connection:
            self._connection = DriverRemoteConnection(self.endpoint, 'g')
            self._g = Graph().traversal().withRemote(self._connection)
        return self._g
    
    def close(self):
        """关闭连接"""
        if self._connection:
            self._connection.close()
            self._connection = None
            self._g = None
            
    def __enter__(self):
        return self.g
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# 全局实例（支持单例模式）
db = GremlinDB()