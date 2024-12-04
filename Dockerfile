# Use a lightweight Python image with version 3.10
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy your application files
COPY . /app

# Install dependencies and LibreOffice
RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies using the generated requirements file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Optional: Install fonts (if necessary)
RUN apt-get update && apt-get install -y \
    ttf-mscorefonts-installer && \
    fc-cache -f -v && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose the port Streamlit will use
EXPOSE 8501

# Set the Streamlit command with the port from $PORT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
