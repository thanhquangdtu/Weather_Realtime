# Real-time Weather Data Engineering Pipeline

Hệ thống thu thập, xử lý và hiển thị dữ liệu thời tiết theo thời gian thực sử dụng Kafka, Spark Streaming, MySQL và Dashboard.

## 📋 Mô tả dự án

Dự án này xây dựng một pipeline data engineering hoàn chỉnh để:
- Thu thập dữ liệu thời tiết từ OpenWeatherMap API
- Streaming data qua Apache Kafka
- Xử lý và transform data bằng Spark Streaming
- Lưu trữ vào MySQL database
- Hiển thị dashboard real-time với Plotly Dash

## 🏗️ Kiến trúc hệ thống

```
Weather API → Producer → Kafka → Spark Streaming → MySQL → Dashboard
```

## 🛠️ Công nghệ sử dụng

- **Apache Kafka**: Message broker
- **Apache Spark**: Stream processing
- **MySQL**: Data storage
- **Plotly Dash**: Visualization dashboard
- **Docker & Docker Compose**: Containerization
- **Python**: Programming language

## 📁 Cấu trúc thư mục

```
├── docker-compose.yml
├── .env
├── README.md
│
├── configs/
│   ├── kafka_config.py
│   ├── mysql_config.py
│   └── settings.py
│
├── producer/
│   ├── __init__.py
│   ├── weather_api.py
│   ├── kafka_producer.py
│   ├── main.py
│   └── requirements.txt
│
├── spark/
│   ├── __init__.py
│   ├── schema.py
│   ├── transform.py
│   ├── spark_stream.py
│   └── requirements.txt
│
├── database/
│   ├── init.sql
│   └── models.py
│
├── dashboard/
│   ├── __init__.py
│   ├── db_connector.py
│   ├── charts.py
│   ├── app.py
│   └── requirements.txt
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
└── data/
    └── sample.json
```

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

## 📊 Services và Ports

| Service | Port | Mô tả |
|---------|------|-------|
| Kafka | 29092 | Kafka broker |
| Zookeeper | 2181 | Kafka coordination |
| MySQL | 3306 | Database |
| Spark Master UI | 8080 | Spark cluster UI |
| Spark Master | 7077 | Spark master |
| Dashboard | 8050 | Plotly Dash web UI |

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

## 📝 Sử dụng

### Producer
Producer sẽ tự động:
- Gọi Weather API theo interval định sẵn
- Parse và validate data
- Publish messages vào Kafka topic

### Spark Streaming
Spark job sẽ:
- Subscribe Kafka topic
- Apply transformations
- Write vào MySQL theo batch

### Dashboard
Dashboard hiển thị:
- Nhiệt độ theo thời gian
- Độ ẩm, tốc độ gió
- Dữ liệu real-time từ database

## 🧪 Testing

```bash
# Test producer
cd producer
python -m pytest tests/

# Test spark transformations
cd spark
python -m pytest tests/
```

## 📈 Monitoring

- **Spark UI**: http://localhost:8080
- **Kafka logs**: `docker logs kafka`
- **MySQL logs**: `docker logs mysql`

## 🛑 Dừng hệ thống

```bash
docker-compose down
```

Để xóa cả volumes (data):

```bash
docker-compose down -v
```

## 🤝 Đóng góp

Pull requests are welcome! For major changes, please open an issue first.

## 📄 License

MIT License

## 👤 Tác giả

Thành Quang

## 🙏 Acknowledgments

- OpenWeatherMap API
- Apache Kafka
- Apache Spark
- Plotly Dash
