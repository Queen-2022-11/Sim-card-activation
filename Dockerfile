# Use the official slim Python image
FROM python:3.11-slim

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the environment variable for Python
ENV PYTHONUNBUFFERED 1

# Command to run your application (modify as needed)
CMD ["python", "app.py"]
