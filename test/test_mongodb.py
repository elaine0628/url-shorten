import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from db.db import init_db, insert_url, fetch_url_by_short

# Mock MongoDB 連接
@pytest.fixture
def mock_mongo():
    with patch('db.db.MongoClient') as mock_client:
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        yield mock_collection

def test_init_db(mock_mongo):
    """測試資料庫初始化"""
    init_db()
    
    # 驗證建立了正確的索引
    mock_mongo.create_index.assert_any_call("short_url", unique=True)
    mock_mongo.create_index.assert_any_call("expiration_date", expireAfterSeconds=0)

def test_insert_url(mock_mongo):
    """測試插入 URL"""
    original_url = "https://example.com"
    short_url = "abc123"
    expiration_date = "2025-01-01T00:00:00"
    
    insert_url(original_url, short_url, expiration_date)
    
    # 驗證 insert_one 被呼叫
    mock_mongo.insert_one.assert_called_once()
    
    # 驗證插入的文件內容
    call_args = mock_mongo.insert_one.call_args[0][0]
    assert call_args["original_url"] == original_url
    assert call_args["short_url"] == short_url
    assert isinstance(call_args["expiration_date"], datetime)
    assert call_args["created_at"] is not None

def test_fetch_url_by_short_found(mock_mongo):
    """測試查詢存在的短網址"""
    original_url = "https://example.com"
    expiration_date = datetime(2025, 1, 1)
    
    mock_mongo.find_one.return_value = {
        "original_url": original_url,
        "expiration_date": expiration_date
    }
    
    result = fetch_url_by_short("abc123")
    
    assert result is not None
    assert result[0] == original_url
    assert result[1] == expiration_date.isoformat()
    
    # 驗證查詢參數
    mock_mongo.find_one.assert_called_once_with(
        {"short_url": "abc123"},
        {"original_url": 1, "expiration_date": 1, "_id": 0}
    )

def test_fetch_url_by_short_not_found(mock_mongo):
    """測試查詢不存在的短網址"""
    mock_mongo.find_one.return_value = None
    
    result = fetch_url_by_short("nonexistent")
    
    assert result is None 