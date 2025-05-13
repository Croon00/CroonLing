# ✅ 1️⃣ Python 3.12 기반 bullseye 이미지 사용
FROM python:3.12-bullseye

# ✅ 2️⃣ 작업 디렉토리 설정
WORKDIR /app

# ✅ 3️⃣ 의존성 설치
COPY requirements.txt .  
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    --no-install-recommends && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# ✅ 4️⃣ 환경 변수 설정 (로그 즉시 출력)
ENV PYTHONUNBUFFERED=1

# ✅ 5️⃣ 소스 코드 복사
COPY . .

# ✅ 6️⃣ 실행할 명령어 설정
CMD ["python", "-u", "main.py"]
