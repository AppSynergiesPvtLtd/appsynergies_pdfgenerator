# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port that the Streamlit app will run on
EXPOSE 8080

# Set environment variables for Streamlit
ENV PORT 8080
ENV STREAMLIT_SERVER_PORT 8080
ENV STREAMLIT_SERVER_HEADLESS true
ENV STREAMLIT_SERVER_ENABLE_CORS false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION false

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
