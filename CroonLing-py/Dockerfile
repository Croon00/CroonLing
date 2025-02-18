# 1️⃣ Python 3.12 기반의 Docker 이미지 사용
FROM python:3.12-slim

# 2️⃣ 작업 디렉토리 설정
WORKDIR /app

# 3️⃣ 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ 의존성 파일 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ 소스 코드 복사
COPY . .

# 6️⃣ 환경 변수 설정 (MongoDB 연결을 위한 URI)
ENV MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/croonling_db?retryWrites=true&w=majority"

# 7️⃣ 실행할 명령어 설정
CMD ["python", "main.py"]
