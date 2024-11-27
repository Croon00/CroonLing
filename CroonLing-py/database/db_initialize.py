from pymysql import connect, MySQLError
from config_loader import load_config

# config.json 파일에서 DB 설정 정보 불러오기
config = load_config()

# AWS RDS MySQL 연결
connection = connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    port=config['port']
)

try:
    with connection.cursor() as cursor:
        # croonling_db 데이터베이스가 없는 경우 생성
        create_db_query = "CREATE DATABASE IF NOT EXISTS croonling_db"
        cursor.execute(create_db_query)

        # croonling_db 사용하도록 설정
        use_db_query = "USE croonling_db"
        cursor.execute(use_db_query)

        # songs 테이블 생성
        create_table_query = """
        CREATE TABLE IF NOT EXISTS songs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            artist VARCHAR(255) NOT NULL,
            song VARCHAR(255) NOT NULL,
            lyrics TEXT NOT NULL,
            translated_lyrics TEXT,
            phonetics_lyrics TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
finally:
    connection.close()
