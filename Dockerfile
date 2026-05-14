FROM python:3.12-slim

RUN useradd --create-home app
WORKDIR /home/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY cache_handler.py media_rpc.py ./
COPY discord_connection/ discord_connection/
COPY media_server_connection/ media_server_connection/

USER app

CMD ["python", "-u", "media_rpc.py"]
