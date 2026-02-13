
## � Kiến trúc hệ thống

```
Weather API → Producer → Kafka → Consumer → MySQL
                          ↑
                     Zookeeper
```

**Luồng dữ liệu:**
1. **Producer** fetch weather data từ OpenWeatherMap API
2. **Producer** gửi data vào **Kafka** (topic: weather_data)
3. **Kafka** lưu trữ messages (với sự hỗ trợ của **Zookeeper**)
4. **Consumer** đọc messages từ **Kafka**
5. **Consumer** insert data vào **MySQL** database

## 🚀 Hướng dẫn cài đặt

### 1. Cấu hình môi trường

Sao chép file `.env` và cập nhật thông tin:

```bash
cp .env.example .env
```

Cập nhật `WEATHER_API_KEY` với API key từ [OpenWeatherMap](https://openweathermap.org/api)

### 2. Khởi động Docker containers (Kafka + Zookeeper + MySQL)

```bash
docker-compose up -d
```

Kiểm tra containers đang chạy:

```bash
docker-compose ps
```

### 3. Chạy Producer (Gửi data vào Kafka)

```bash
cd producer
pip install -r requirements.txt
python main.py
```

Producer sẽ fetch weather data từ API và gửi vào **Kafka topic: weather_data**

### 4. Chạy Consumer (Đọc từ Kafka và lưu vào MySQL)

```bash
cd consumer
pip install -r requirements.txt
python kafka_consumer.py
```

Consumer sẽ đọc messages từ **Kafka** và insert vào **MySQL database**



## 🔧 Cấu hình

### Weather API
- Lấy API key miễn phí tại: https://openweathermap.org/api
- Cập nhật `WEATHER_API_KEY` trong file `.env`
- Cấu hình danh sách thành phố trong `CITIES`

### Kafka
- Bootstrap servers: `localhost:29092`
- Topic: `weather_data`
- Auto-create topics: enabled

### MySQL
- Database: `weather_db`
- Schema được khởi tạo tự động từ `database/init.sql`

## Testing
```bash
# Test producer
cd producer
python -m pytest tests/

# Test spark transformations
cd spark
python -m pytest tests/
```



