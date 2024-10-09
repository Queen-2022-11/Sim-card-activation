# Use a compatible Python version
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt first for caching
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "app.py"]
