FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY discord_api/ discord_api/
COPY media_rpc.py .

CMD ["python", "-u", "media_rpc.py"]
