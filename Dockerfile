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

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download and install Google Fonts manually
RUN wget https://github.com/google/fonts/archive/main.zip -O /tmp/fonts.zip && \
    unzip /tmp/fonts.zip -d /usr/share/fonts && \
    rm /tmp/fonts.zip && \
    fc-cache -f -v

# Expose the port Streamlit will use
EXPOSE 8501

# Set the Streamlit command with the port from $PORT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
