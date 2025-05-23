# ✅ 1️⃣ Python 3.12 기반 이미지
FROM python:3.12-bullseye

# ✅ 2️⃣ 작업 디렉토리
WORKDIR /app

# ✅ 3️⃣ 의존성 설치
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    --no-install-recommends && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# ✅ 4️⃣ 환경 변수
ENV PYTHONUNBUFFERED=1

# ✅ 5️⃣ 소스 복사
COPY . .

# ✅ 6️⃣ FastAPI 서버로 실행 (포트 8000)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
