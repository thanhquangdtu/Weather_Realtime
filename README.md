
## 🚀 Hướng dẫn cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd Weather_realtime
```

### 2. Cấu hình môi trường

Sao chép file `.env` và cập nhật thông tin:

```bash
cp .env.example .env
```

Cập nhật `WEATHER_API_KEY` với API key từ [OpenWeatherMap](https://openweathermap.org/api)

### 3. Khởi động Docker containers

```bash
docker-compose up -d
```

Kiểm tra containers đang chạy:

```bash
docker-compose ps
```

### 4. Chạy Producer

```bash
cd producer
pip install -r requirements.txt
python main.py
```

### 5. Chạy Spark Streaming

```bash
cd spark
pip install -r requirements.txt
python spark_stream.py
```

### 6. Truy cập Dashboard

Mở trình duyệt và truy cập: `http://localhost:8050`

## 🔧 Cấu hình

### Weather API
- Lấy API key miễn phí tại: https://openweathermap.org/api
- Cập nhật `WEATHER_API_KEY` trong file `.env`
- Cấu hình danh sách thành phố trong `CITIES`

### Kafkaw1
- Bootstrap servers: `localhost:29092`
- Topic: `weather_data`
- Auto-create topics: enabled

### MySQL
- Database: `weather_db`
- Schema được khởi tạo tự động từ `database/init.sql`

## 🧪 Testing
```bash
# Test producer
cd producer
python -m pytest tests/

# Test spark transformations
cd spark
python -m pytest tests/
```



