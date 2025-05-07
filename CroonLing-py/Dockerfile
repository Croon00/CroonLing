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
    fonts-noto-cjk \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# ✅ 4️⃣ setuptools, packaging 설치
RUN pip install --upgrade pip setuptools wheel packaging

# ✅ 5️⃣ requirements.txt 패키지 설치
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 6️⃣ 환경 변수 설정 (로그 즉시 출력)
ENV PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    CHROME_BINARY=/usr/bin/chromium

# ✅ 7️⃣ 소스 코드 복사
COPY . .

# ✅ 8️⃣ 실행할 명령어 설정
CMD ["python", "-u", "main.py"]
