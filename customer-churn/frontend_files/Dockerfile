# Use a lightweight official Python 3.9 runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container's file system to /app
WORKDIR /app

# Copy all local files and directories from the host frontend workspace into the container at /app
COPY . .

# Install the necessary frontend dependencies defined in the requirements file
RUN pip3 install -r requirements.txt

# Expose the default Streamlit application port
EXPOSE 8501

# Start the Streamlit server on interface 0.0.0.0, port 8501, disabling cross-site request forgery protection
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
