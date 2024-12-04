FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy application files
COPY . /app

# Install LibreOffice and other required packages
RUN apt-get update && \
    apt-get install -y libreoffice curl fonts-liberation && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Google Fonts
RUN pip install googlefonts-installer && \
    googlefonts-installer install "Liberation Sans" "Arial" --skip-on-missing

# Refresh the font cache to make sure the fonts are available
RUN fc-cache -f -v

# Expose the port the Streamlit app will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
