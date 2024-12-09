from pymysql import connect, MySQLError
from config_loader import load_config

config = load_config()

def initialize_db():
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


            # # 각 테이블 드롭 쿼리
            # drop_songs_name_kr_query = "DROP TABLE IF EXISTS songs_name_kr"
            # cursor.execute(drop_songs_name_kr_query)

            # drop_songs_query = "DROP TABLE IF EXISTS songs"
            # cursor.execute(drop_songs_query)

            # drop_artist_kr_query = "DROP TABLE IF EXISTS artist_kr"
            # cursor.execute(drop_artist_kr_query)

            # drop_artists_query = "DROP TABLE IF EXISTS artists"
            # cursor.execute(drop_artists_query)




            # artists 테이블 생성
            create_artists_query = """
            CREATE TABLE IF NOT EXISTS artists (
                artist_id VARCHAR(255) PRIMARY KEY,  -- Spotify에서 받은 아티스트 고유 ID 사용
                artist_name VARCHAR(255) NOT NULL
            )
            """
            cursor.execute(create_artists_query)

            # artist_kr 테이블 생성
            create_artist_kr_query = """
            CREATE TABLE IF NOT EXISTS artist_kr (
                artist_kr_id INT AUTO_INCREMENT PRIMARY KEY,
                artist_id VARCHAR(255),  -- Spotify 고유 ID를 외래키로 참조
                artist_kr_name VARCHAR(255),  -- 여러 한국어 이름을 저장 가능, NOT NULL 제약 제거
                FOREIGN KEY (artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE
            )
            """
            cursor.execute(create_artist_kr_query)

            # songs 테이블 생성
            create_songs_query = """
            CREATE TABLE IF NOT EXISTS songs (
                song_id VARCHAR(255) PRIMARY KEY,  -- Spotify에서 받은 트랙 고유 ID 사용
                song_name VARCHAR(255),  -- 곡 제목 추가
                lyrics TEXT,  -- 가사에 NOT NULL 제약 조건 제거
                translated_lyrics TEXT,
                phonetics_lyrics TEXT,
                korean_phonetics_lyrics TEXT,
                release_date DATE,  -- 트랙 발매일
                track_image_url VARCHAR(2083),  -- 트랙의 이미지 URL 저장
                album_name VARCHAR(255),  -- 앨범 이름 추가
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                artist_id VARCHAR(255),  -- 아티스트 ID를 외래키로 참조
                FOREIGN KEY (artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE
            )
            """
            cursor.execute(create_songs_query)

            # songs_name_kr 테이블 생성
            create_songs_name_kr_query = """
            CREATE TABLE IF NOT EXISTS songs_name_kr (
                songs_name_kr_id INT AUTO_INCREMENT PRIMARY KEY,
                song_id VARCHAR(255),  -- Spotify 고유 ID를 외래키로 참조
                song_name_kr VARCHAR(255),  -- 여러 한국어 곡 이름 저장 가능, NOT NULL 제약 제거
                FOREIGN KEY (song_id) REFERENCES songs(song_id) ON DELETE CASCADE
            )
            """
            cursor.execute(create_songs_name_kr_query)


            
            # `song_name` 컬럼 존재 여부 확인 및 추가
            check_song_name_column_query = """
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'croonling_db' AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'song_name'
            """
            cursor.execute(check_song_name_column_query)
            if cursor.fetchone()[0] == 0:
                alter_song_name_query = """
                ALTER TABLE songs ADD COLUMN song_name VARCHAR(255) AFTER song_id;
                """
                cursor.execute(alter_song_name_query)
                print("song_name 컬럼이 성공적으로 추가되었습니다.")
                
    
            # `release_date` 컬럼 존재 여부 확인 및 추가
            check_release_date_column_query = """
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'croonling_db' AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'release_date'
            """
            cursor.execute(check_release_date_column_query)
            if cursor.fetchone()[0] == 0:
                alter_release_date_query = """
                ALTER TABLE songs ADD COLUMN release_date DATE AFTER korean_phonetics_lyrics;
                """
                cursor.execute(alter_release_date_query)
                print("release_date 컬럼이 성공적으로 추가되었습니다.")

            # `album_name` 컬럼 존재 여부 확인 및 추가
            check_album_name_column_query = """
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'croonling_db' AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'album_name'
            """
            cursor.execute(check_album_name_column_query)
            if cursor.fetchone()[0] == 0:
                alter_album_name_query = """
                ALTER TABLE songs ADD COLUMN album_name VARCHAR(255) AFTER track_image_url;
                """
                cursor.execute(alter_album_name_query)
                print("album_name 컬럼이 성공적으로 추가되었습니다.")
                
                
            connection.commit()
            print("DB 초기화가 완료되었습니다.")
    except MySQLError as e:
        print(f"DB 초기화 중 오류 발생: {str(e)}")
    finally:
        connection.close()
