FROM python:3.9

# Install C compiler and Java
RUN apt-get update && apt-get install -y \
    gcc \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
