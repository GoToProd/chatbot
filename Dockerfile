FROM python:3.12

WORKDIR /chatgpt
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt
COPY Bot/ ./Bot
CMD ["python", "Bot/main.py"]
