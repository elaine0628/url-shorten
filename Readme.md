# URL Shortener API Documentation

## Overview
This API provides a simple URL shortening service. Users can create short URLs that redirect to their original URLs.

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
  "error_code": 0,
  "data": {
    "short_url": "abc123",
    "expiration_date": "2025-04-30T12:00:00",
    "success": true
  }
}
```

### **Errors:**
| Status Code | error_code | data                   |
|-------------|------------|------------------------|
| 200         |600         | Invalid URL format     |
| 200         |601         | URL is too long        |

### **Example Response:**
```json
{
  "error_code": 600,
  "data": "Invalid URL format"
}
```
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
| Status Code | error_code | data                   |
|-------------|------------|------------------------|
| 200         |602         | Short URL not found    |
| 200         |603         | Short URL expired      |

### **Example Response:**
```json
{
  "error_code": 602,
  "data": "Short URL not found"
}
```
---

## **How to Run with Docker**

### **Prerequisites**
Make sure MongoDB is running on your system or in a container.

### **Build and Run**
1. **Build the Docker Image:**
   ```sh
   docker build -t url-shortener .
   ```
2. **Run the Container:**
   ```sh
   docker run -p 4000:4000 -e MONGO_URI=mongodb://host.docker.internal:27017/ -d url-shortener
   ```
   or if MongoDB is on the same host:
   ```sh
   docker run -p 4000:4000 --network host -d url-shortener
   ```
3. **Access API Docs:**
   - Swagger UI: [http://127.0.0.1:4000/docs](http://127.0.0.1:4000/docs)
   - ReDoc: [http://127.0.0.1:4000/redoc](http://127.0.0.1:4000/redoc)

---

## **Settings**

The application can be configured using a YAML settings file and environment variables.

### **setting/settings.yaml**

```yaml
app:
  port: 4000
```

### **Override with Environment Variables**

You can override the port with the `PORT` environment variable:

```sh
PORT=8080 python3 main.py
```

You can also configure MongoDB connection with the `MONGO_URI` environment variable:

```sh
MONGO_URI=mongodb://localhost:27017/ python3 main.py
```

## **Development & Testing**

### **Installation**
```bash
make install     # Install dependencies
```

### **Running Tests**
```bash
make test        # Run all tests with verbose output
make coverage    # Run tests with coverage report
make clean       # Clean up cache files and reports
```

### **Test Coverage**
Current test coverage: **95%**
- ✅ API handlers: 100%
- ✅ Database operations: 100%
- ✅ Data models: 100%
- ⚠️ Main application: 0% (entry point)
- ⚠️ Utils: 75%

### **Test Structure**
```
test/
├── test_mongodb.py    # Database operation tests
└── test_shorten.py    # API handler tests
```

### **Running Individual Tests**
```bash
# Run specific test file
python -m pytest test/test_shorten.py -v

# Run specific test function
python -m pytest test/test_shorten.py::test_create_short_url_success -v

# Run with coverage for specific file
python -m pytest test/test_mongodb.py --cov=db --cov-report=term-missing
```

---

## **Project Structure**

```
url-shortener/
├── api/
│   ├── api.py         # Route registration
│   ├── shorten.py     # Handler functions
├── config/
│   └── config.py      # Load YAML and env config
├── db/
│   └── db.py          # Database logic
├── models/
│   ├── schema.py      # Pydantic models
│   └── errcode.py     # Error codes
├── server/
│   ├── server.py      # App factory and middleware
├── utils/
│   └── utils.py       # Short URL generator, helpers
├── setting/
│   └── setting.yaml   # YAML config
├── test/
│   ├── test_mongodb.py # Database operation tests
│   └── test_shorten.py # API handler tests
├── main.py             # Entrypoint
├── requirements.txt
├── pytest.ini         # Pytest configuration
├── makefile           # Development commands
├── Dockerfile
├── .gitignore
└── README.md
```

---

## **License**
This API is open-source and free to use. Contributions are welcome!
