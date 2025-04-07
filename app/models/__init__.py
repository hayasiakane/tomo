from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
import uuid
from datetime import datetime

class GremlinDB:
    def __init__(self, endpoint=None):
        self.endpoint = endpoint or "ws://localhost:8182/gremlin"
        self.graph = Graph()
        self.connection = None
        self.g = None
        
    def init_app(self, app):
        self.endpoint = app.config.get('GREMLIN_SERVER_URL', self.endpoint)
        self.connect()
        
    def connect(self):
        self.connection = DriverRemoteConnection(self.endpoint, 'g')
        self.g = self.graph.traversal().withRemote(self.connection)
        
    def close(self):
        if self.connection:
            self.connection.close()
# 全局数据库实例
db = GremlinDB()