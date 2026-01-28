FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
COPY . /app
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
