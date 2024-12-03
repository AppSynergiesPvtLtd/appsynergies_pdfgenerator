# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy your application files
COPY . /app

# Install dependencies and LibreOffice
RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit will use
EXPOSE 8080

# Set the Streamlit command with the port from $PORT
CMD ["streamlit", "run", "app.py", "--server.port=$PORT", "--server.headless=true"]
