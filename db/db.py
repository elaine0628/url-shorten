from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB 連接設定
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "url_shortener"
COLLECTION_NAME = "urls"

def get_db():
    """取得 MongoDB 資料庫連接"""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def get_collection():
    """取得 URLs 集合"""
    db = get_db()
    return db[COLLECTION_NAME]

def init_db():
    """初始化資料庫 - 在 MongoDB 中建立索引"""
    collection = get_collection()
    
    # 建立唯一索引確保 short_url 不重複
    collection.create_index("short_url", unique=True)
    
    # 建立 TTL 索引自動刪除過期的文件
    collection.create_index("expiration_date", expireAfterSeconds=0)

def insert_url(original_url: str, short_url: str, expiration_date: str):
    """插入新的 URL 記錄"""
    collection = get_collection()
    
    # 將 expiration_date 字串轉換為 datetime 物件
    expiration_datetime = datetime.fromisoformat(expiration_date)
    
    document = {
        "original_url": original_url,
        "short_url": short_url,
        "expiration_date": expiration_datetime,
        "created_at": datetime.utcnow()
    }
    
    collection.insert_one(document)

def fetch_url_by_short(short_url: str):
    """根據短網址查詢原始網址"""
    collection = get_collection()
    
    # 查詢文件，只返回需要的欄位
    document = collection.find_one(
        {"short_url": short_url},
        {"original_url": 1, "expiration_date": 1, "_id": 0}
    )
    
    if document:
        # 將 datetime 轉回 ISO 字串格式以保持 API 相容性
        return (
            document["original_url"],
            document["expiration_date"].isoformat()
        )
    
    return None
