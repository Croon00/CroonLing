# ✅ 1️⃣ Python 3.12 기반 bullseye 이미지 사용
FROM python:3.12-bullseye

# ✅ 2️⃣ 작업 디렉토리 설정
WORKDIR /app

# ✅ 3️⃣ 필요한 패키지 설치 (Chrome Dependencies)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    xauth \ 
    fonts-noto-cjk \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# ✅ 4️⃣ 최신 Chrome 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# ✅ 5️⃣ ChromeDriver 수동 설치
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

# ✅ 6️⃣ setuptools, packaging 설치
RUN pip install --upgrade pip setuptools wheel packaging

# ✅ 7️⃣ requirements.txt 패키지 설치
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# ✅ 8️⃣ 환경 변수 설정 (로그 즉시 출력)
ENV PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    CHROME_BINARY=/usr/bin/google-chrome

# ✅ 9️⃣ 소스 코드 복사
COPY . .

# ✅ 10️⃣ 실행할 명령어 설정
CMD ["run", "-a", "python", "-u", "main.py"]
