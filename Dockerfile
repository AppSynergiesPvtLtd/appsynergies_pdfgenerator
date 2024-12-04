# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy your application files
COPY . /app

# Install dependencies and LibreOffice
RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-writer fonts-liberation wget unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and install Google Fonts
RUN wget -O /tmp/roboto.zip "https://github.com/google/fonts/raw/main/apache/roboto/Roboto%5Bwdth%2Cwght%5D.ttf" && \
    mkdir -p /usr/share/fonts/truetype/roboto && \
    mv /tmp/roboto.zip /usr/share/fonts/truetype/roboto/Roboto-Regular.ttf && \
    fc-cache -f -v && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit will use
EXPOSE 8501

# Set the Streamlit command with the port from $PORT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
