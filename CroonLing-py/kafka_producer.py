from pymongo import MongoClient
from kafka import KafkaProducer
import json
import threading
import time

from config_loader import load_config

# ✅ 설정 로드 및 DB 연결
config = load_config()
client = MongoClient(config.get('MONGO_URI'))
db = client["croonling"]

# ✅ Kafka 설정
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

def send_to_kafka(topic, data):
    producer.send(topic, data)
    print(f"📤 Sent to Kafka ({topic}): {data}")

def listen_collection(db, collection_name, topic):
    resume_token = None
    while True:
        try:
            if resume_token:
                stream = db[collection_name].watch(resume_after=resume_token)
            else:
                stream = db[collection_name].watch(full_document='updateLookup')
            for change in stream:
                resume_token = change['_id']
                operation_type = change['operationType']
                if operation_type in ['insert', 'update']:
                    doc = change['fullDocument']
                    doc["_id"] = str(doc["_id"])  # ObjectId 문자열로 변환
                    send_to_kafka(topic, doc)
                elif operation_type == 'delete':
                    doc_id = str(change['documentKey']['_id'])
                    send_to_kafka(topic, {"delete": doc_id})
                else:
                    print(f"[WARN] Unknown operation type: {operation_type}")
        except Exception as e:
            print(f"[ERROR] Change Stream Error: {e}. Resuming with last token: {resume_token}")
            time.sleep(5)

# ✅ 쓰레드 등록: songs, artists, lyrics 모두 감시
thread_songs = threading.Thread(target=listen_collection, args=(db, "songs", "song-events"))
thread_artists = threading.Thread(target=listen_collection, args=(db, "artists", "artist-events"))
thread_lyrics = threading.Thread(target=listen_collection, args=(db, "lyrics", "lyrics-events"))

thread_songs.start()
thread_artists.start()
thread_lyrics.start()

# ✅ 메인 쓰레드 유지
while True:
    time.sleep(1)
