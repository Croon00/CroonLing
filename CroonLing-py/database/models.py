from mongoengine import Document, StringField, connect

# MongoDB 연결
connect("croonling_db", host="mongodb://localhost:27017")

# 아티스트 모델 (MongoDB)
class Artist(Document):
    artist_id = StringField(required=True, unique=True)
    artist_name = StringField(required=True)

# 데이터 삽입
artist = Artist(artist_id="123", artist_name="BTS")
artist.save()

# 데이터 조회
artist = Artist.objects(artist_id="123").first()
print(artist.artist_name)
