# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy your application files
COPY . /app

# Install dependencies including LibreOffice, curl, and fonts
RUN apt-get update && \
    apt-get install -y curl libreoffice libreoffice-writer fonts-liberation unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download Google Fonts directly
RUN curl -L -o /usr/share/fonts/truetype/roboto.zip https://fonts.google.com/download?family=Roboto && \
    unzip /usr/share/fonts/truetype/roboto.zip -d /usr/share/fonts/truetype/roboto/ && \
    fc-cache -f -v && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose the port Streamlit will use
EXPOSE 8501

# Set the Streamlit command with the port from $PORT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
