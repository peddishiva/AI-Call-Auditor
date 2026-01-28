# Call Auditor – Dockerized Streamlit App

This guide explains how to fork the repository, build the Docker image, and run the Streamlit application using Docker.

---

## 1. Fork and Clone the Repository

First, fork this repository to your own GitHub account.

Then clone your fork locally:

```
git clone <your-forked-repo-url>
cd <project-directory>
```

---
## 2. Create a file named Dockerfile in the root of the project with the following content:

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
---

## 3. From the project root directory, run:

```
docker build -t call-auditor .
```
---
## 4. Start the application with the following command:

```
docker run --rm -it \
  -p 8501:8501 \
  -v "C:\path\to\your\local\folder:/call-auditor/app" \
  --name call-auditor-container \
  call-auditor:latest
```
---
## 5. Once the container is running, open your browser and go to:

http://localhost:8501

---
