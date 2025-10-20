# DeepFace API Documentation

References: https://github.com/serengil/deepface

## 📋 Overview

DeepFace API is an intelligent facial recognition system using advanced AI technology, providing the following features:

- **🔍 Process**: Process and temporarily store face images with anti-spoofing checks
- **📝 Register**: Register user faces into the database system
- **✅ Verify**: Authenticate user faces with high accuracy

### ✨ Key Features

- **Anti-Spoofing**: Detect and prevent fake images and videos
- **High Accuracy**: Uses GhostFaceNet with high precision
- **Real-time Processing**: Fast processing with Redis caching
- **Scalable**: Supports multiple concurrent users

## 🚀 Installation and Deployment

### 📋 System Requirements

| Component   | Version | Description                |
| ----------- | ------- | -------------------------- |
| **Python**  | 3.10 +  | Runtime environment        |
| **MySQL**   | 8.0+    | Main database              |
| **Redis**   | 7.0+    | Cache and session storage  |
| **RAM**     | 4GB+    | Recommended for production |
| **Storage** | 10GB+   | For models and data        |

### 🔧 Install Dependencies

```bash
# Clone repository
git clone https://github.com/NguyenThong251/deepface.git
cd deepface

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### ⚙️ Configuration

#### 1. Database Configuration (`src/config/sql.py`)

```python
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'deepface_db',
    'port': 3306
}
```

#### 2. Redis Configuration (`src/config/redis.py`)

```python
redis_config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True
}
```

#### 3. Create Database Schema

```sql
CREATE DATABASE deepface_db;
USE deepface_db;

CREATE TABLE face (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    image_face LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🏃‍♂️ Run Application

#### Development Mode

```bash
python app.py
```

#### Production Mode

```bash
gunicorn --bind 0.0.0.0:5005 --workers 4 app:app
```

## 🔌 API Endpoints

### 🌐 Base URL

```
POST /face/api
```

### 📝 Request Format

All requests use JSON format with standard structure:

```json
{
  "_operation": "deepface", // Module name (required)
  "mode": "process|register|verify|search", // Function type (required)
  "user_id": "string", // User identifier (required for process/register/verify)
  "image": "base64_string" // Base64 image (required for process/verify/search)
}
```

### 📊 Response Format

#### ✅ Success Response

```json
{
  "success": true,
  "result": {
    "code": "OK",
    "message": true
  }
}
```

#### ❌ Error Response

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

---

## 🔍 1. Process Endpoint

### 📋 Description

Process face images with anti-spoofing checks and temporarily store in Redis cache.

**Endpoint**: `POST /face/api`  
**Mode**: `process`

### 📤 Request

```json
{
  "_operation": "deepface",
  "mode": "process",
  "user_id": "user123",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

### 🔄 Detailed Workflow

#### 1️⃣ **Validation Phase**

```mermaid
graph TD
    A[Request] --> B{user_id exists?}
    B -->|No| C[VALIDATION_FAILED]
    B -->|Yes| D{image exists?}
    D -->|No| C
    D -->|Yes| E[Next Phase]
```

## 📝 2. Register Endpoint

### 📋 Description

Register user face into database from processed image stored in Redis cache.

**Endpoint**: `POST /face/api`  
**Mode**: `register`

### 📤 Request

```json
{
  "_operation": "deepface",
  "mode": "register",
  "user_id": "user123"
}
```

## ✅ 3. Verify Endpoint

### 📋 Description

Authenticate user face by comparing with registered face in database.

**Endpoint**: `POST /face/api`  
**Mode**: `verify`

### 📤 Request

```json
{
  "_operation": "deepface",
  "mode": "verify",
  "user_id": "user123",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

## 🔍 4. Search Endpoint

### 📋 Description

Search for users by face image using vector database (Qdrant). Coming soon

**Endpoint**: `POST /face/api`  
**Mode**: `search`

### 📤 Request

```json
{
  "_operation": "deepface",
  "mode": "search",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

## 🚨 Error Codes Reference (Based on Actual Code)

| Code                 | Applies to              | Description                    |
| -------------------- | ----------------------- | ------------------------------ |
| `VALIDATION_FAILED`  | Process/Register/Verify | Missing required parameters    |
| `ALREADY_REGISTERED` | Process/Register        | User already registered        |
| `NOT_REGISTERED`     | Verify                  | User not registered            |
| `SAVE_FAILED`        | Process/Register        | Failed to save to Redis or SQL |
| `NO_FACE_FOUND`      | Search                  | No face found in database      |
| `SYSTEM ERROR`       | All                     | General system error           |

## 🛠️ Technology Stack

### 🤖 AI Models

| Model            | Version | Purpose            | Accuracy |
| ---------------- | ------- | ------------------ | -------- |
| **YOLO**         | v12n    | Face Detection     | 99.2%    |
| **FasNet**       | Latest  | Anti-Spoofing      | 98.5%    |
| **GhostFaceNet** | Latest  | Facial Recognition | 99.7%    |

### 🏗️ Infrastructure Stack

| Component            | Technology         | Purpose                |
| -------------------- | ------------------ | ---------------------- |
| **Backend**          | Flask + Gunicorn   | API Server             |
| **Database**         | MySQL 8.0+         | Data Storage           |
| **Cache**            | Redis 7.0+         | Session & Temp Storage |
| **Image Processing** | OpenCV + NumPy     | Image Manipulation     |
| **AI Framework**     | TensorFlow + Keras | Model Inference        |

### 📸 Image Requirements

| Parameter      | Requirement               | Notes                    |
| -------------- | ------------------------- | ------------------------ |
| **Format**     | Base64 encoded            | JPEG/PNG recommended     |
| **Size**       | 80KB < size < 100KB       | Optimal for processing   |
| **Resolution** | Min 224x224px             | Model input requirement  |
| **Quality**    | High contrast, clear face | Avoid blurry/dark images |
| **Face Ratio** | 30-70% of image           | Face should be prominent |

---

## ⚠️ Important Notes

### 🔄 Required Process Flow

1. **Execution order**: `Process` → `Register` → `Verify`
2. **Cache time**: Temporary images in Redis have TTL 600 seconds (10 minutes)
3. **Session timeout**: Must register within 10 minutes after process

### 🛡️ Security

- **Anti-spoofing**: All images are checked for anti-spoofing
- **Authentication**: Can be enabled by uncommenting `@require_auth`
- **Data encryption**: Images are encrypted in database

### ⚡ Performance

- **Redis caching**: Optimizes processing speed
- **Model optimization**: Uses GPU if available
- **Concurrent requests**: Supports multiple simultaneous requests

### 🔧 Environment Variables

```bash
# Database
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=deepface_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Application
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## 🖥️ VPS Deployment Guide

### 📋 Prerequisites

1. **Python Manager**: Install Python 3.10 < version < 3.12
2. **Database**: Install MySQL and Redis
3. **Web Server**: Setup Nginx/Apache/OpenLiteSpeed/Caddy
4. **Git**: Clone repository

### 🚀 Step-by-Step Deployment

#### 1️⃣ **Clone Repository**

```bash
cd /path/to/your/site
git clone https://github.com/NguyenThong251/deepface.git
cd deepface
```

#### 2️⃣ **Database Setup**

```sql
-- Create database
CREATE DATABASE deepface_db;
CREATE USER 'deepface_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON deepface_db.* TO 'deepface_user'@'localhost';
FLUSH PRIVILEGES;

-- Create table
USE deepface_db;
CREATE TABLE face (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    image_face LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3️⃣ **Python Manager Configuration**

| Setting          | Value                 |
| ---------------- | --------------------- |
| **Name**         | deepface-api          |
| **Version**      | 3.10 < version < 3.12 |
| **Framework**    | Python                |
| **Startup Mode** | Gunicorn              |
| **Project Path** | `/path/to/deepface`   |
| **Start File**   | `app.py`              |
| **Port**         | 5005                  |

#### 4️⃣ **Dependencies Installation**

```bash
# 1. Upgrade pip and tools
sudo ./_venv/bin/python3 -m pip install --upgrade pip setuptools wheel

# 2. Install dependencies
sudo ./_venv/bin/python3 -m pip install -r requirements.txt
```

### 📁 Project Structure

```
deepface/
├── src/                    # Source code
│   ├── config/            # Configuration files
│   ├── models/            # AI models
│   ├── services/          # Business logic
│   └── modules/           # API modules
├── data/                  # Data files
├── logs/                  # Log files
├── tests/                 # Test files
├── docs/                  # Documentation
├── .env                   # Environment variables
├── .env.local            # Local environment
├── requirements.txt       # Dependencies
└── app.py                # Main application
```

### 🔧 Production Notes

#### Requirements.txt Dependencies:

- **Development**: `opencv-python` (GUI support)
- **Production**: `opencv-python-headless` (No GUI, smaller size)

#### Performance Optimization:

```bash
# Install production dependencies
sudo ./_venv/bin/python3 -m pip install opencv-python-headless
sudo ./_venv/bin/python3 -m pip uninstall opencv-python
```

### 🚦 Health Check

```bash
# Test API endpoint
curl -X POST http://localhost:5005/face/api \
  -H "Content-Type: application/json" \
  -d '{"_operation":"deepface","mode":"process","user_id":"test","image":"test"}'
```

### 📊 Monitoring

- **Logs**: Check `logs/` directory
- **Database**: Monitor MySQL performance
- **Redis**: Monitor cache usage
- **System**: Monitor CPU/RAM usage
