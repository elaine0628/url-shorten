FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
COPY setting/setting.yaml /app/setting/setting.yaml

ENV PORT=4000
EXPOSE 4000

CMD ["python", "main.py"]
