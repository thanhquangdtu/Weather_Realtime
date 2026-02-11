FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy parent configs
COPY ../configs /app/configs
COPY ../database /app/database
COPY ../utils /app/utils

# Expose port
EXPOSE 8050

# Run dashboard
CMD ["python", "app.py"]
