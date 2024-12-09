from pymysql import connect
from config_loader import load_config

config = load_config()

class BaseDB:
    def __init__(self):
        self.config = config

    def _get_connection(self):
        """데이터베이스 연결 생성 메서드"""
        return connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database'],
            port=self.config['port']
        )
