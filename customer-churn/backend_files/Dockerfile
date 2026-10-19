# Use a lightweight official Python 3.9 runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container's file system to /app
WORKDIR /app

# Copy the current directory contents (including model, code, etc.) into /app inside the container
COPY . .

# Install the necessary packages specified in requirements.txt without caching downloaded wheels
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose port 7860 to allow communication with the Flask server
EXPOSE 7860

# Launch Gunicorn with 4 workers, binding the app's predictor instance to run on port 7860
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:churn_predictor_api"]
