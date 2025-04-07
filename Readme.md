# URL Shortener API Documentation

## Overview
This API provides a simple URL shortening service. Users can create short URLs that redirect to their original URLs. The service includes expiration handling and rate limiting.

## Base URL
```
http://127.0.0.1:4000
```

---

## **1. Create Short URL**
### **Endpoint:**
```
POST /shorten
```

### **Request Headers:**
| Header       | Value                  |
|-------------|------------------------|
| Content-Type | application/json       |
| Accept       | application/json       |

### **Request Body:**
```json
{
  "original_url": "https://example.com"
}
```

### **Response:**
| Field            | Type    | Description |
|-----------------|--------|-------------|
| short_url       | string | The generated short URL |
| expiration_date | string | Expiration date (ISO 8601 format) |
| success         | bool   | Indicates if the operation was successful |

### **Example Response:**
```json
{
  "short_url": "abc123",
  "expiration_date": "2025-04-30T12:00:00",
  "success": true
}
```

### **Errors:**
| Status Code | Message                |
|------------|------------------------|
| 400        | Invalid URL format     |
| 429        | Rate limit exceeded    |
| 500        | Internal server error  |

---

## **2. Redirect Using Short URL**
### **Endpoint:**
```
GET /{short_url}
```

### **Request Parameters:**
| Parameter   | Type   | Description               |
|------------|--------|---------------------------|
| short_url  | string | The generated short URL  |

### **Response:**
- **Redirects to the original URL** if the short URL is valid and not expired.

### **Errors:**
| Status Code | Message                    |
|------------|----------------------------|
| 404        | Short URL not found        |
| 410        | Short URL expired          |
| 429        | Rate limit exceeded        |

---

## **How to Run with Docker**
1. **Build the Docker Image:**
   ```sh
   docker build -t url-shortener .
   ```
2. **Run the Container:**
   ```sh
   docker run -p 4000:4000 -d url-shortener
   ```
3. **Access API Docs:**
   - Swagger UI: [http://127.0.0.1:4000/docs](http://127.0.0.1:4000/docs)
   - ReDoc: [http://127.0.0.1:4000/redoc](http://127.0.0.1:4000/redoc)

---

## **Rate Limits**
| Endpoint       | Limit            |
|---------------|------------------|
| POST /shorten | 5 requests/minute |
| GET /{short_url} | 10 requests/minute |

---

## **License**
This API is open-source and free to use. Contributions are welcome!
