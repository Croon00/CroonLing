# ✅ 1️⃣ Python 3.12 기반 bullseye 이미지 사용
FROM python:3.12-bullseye

# ✅ 2️⃣ 작업 디렉토리 설정
WORKDIR /app

# ✅ 3️⃣ Chrome 및 드라이버 설치
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# ✅ 4️⃣ requirements.txt 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 5️⃣ 소스 코드 복사
COPY . .

# ✅ 6️⃣ 실행할 명령어 설정
CMD ["python", "main.py"]
