# Use a light Python image 
FROM python:3.9-slim

# Install C, C++ compilers and Java JDK 
# Changed openjdk-17-jdk-headless to default-jdk-headless for better compatibility
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install dependencies [cite: 3, 4]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

# Copy all project files 
COPY . .

# Start the FastAPI server 
# Using the main:app reference from your main.py [cite: 4]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
