# Use a specific Python version
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy your application files
COPY . /app

# Install dependencies and LibreOffice
RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install fonts and Google Fonts
RUN apt-get update && \
    apt-get install -y fonts-liberation ttf-mscorefonts-installer && \
    pip install googlefonts-installer && \
    googlefonts-installer install "Liberation Sans" "Arial" --skip-on-missing && \
    fc-cache -f -v

# Set locale to prevent text rendering issues
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Expose the port Streamlit will use
EXPOSE 8501

# Set the Streamlit command with the port from $PORT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
