FROM python:3.11-slim

# 建立非 root 使用者
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# 先複製 requirements.txt 以利用 Docker 層級快取
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式程式碼
COPY . .

# 變更檔案擁有者
RUN chown -R appuser:appuser /app

# 切換到非 root 使用者
USER appuser

EXPOSE 4000

CMD ["python", "main.py"]
