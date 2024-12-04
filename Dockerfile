# Use a lightweight Python image
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

RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) multiverse" && \
    apt-get update && apt-get install -y ttf-mscorefonts-installer

# Expose the port Streamlit will use
EXPOSE 8501

# Set the Streamlit command with the port from $PORT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
