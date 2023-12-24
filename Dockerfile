FROM python:3.9-slim
ENV TZ Asia/Singapore
WORKDIR /app
COPY requirements.txt /app
RUN apt-get update && apt-get install -y autossh
RUN pip install --no-cache-dir -r requirements.txt
COPY src /app
ENTRYPOINT ["python","main.py"]