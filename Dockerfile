FROM python:3.9-slim

# Install C, C++ compilers and Java JDK 
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies [cite: 3, 4]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files 
COPY . .

# Start the FastAPI server 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
