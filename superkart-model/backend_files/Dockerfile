# Rationale: Using python:3.9-slim as the base image keeps the container lightweight while providing the necessary Python environment.
FROM python:3.9-slim
# Rationale: Setting /app as the working directory inside the container.
WORKDIR /app
# Rationale: Copying all local files (app.py, requirements, model) into the container's /app directory.
COPY . .
# Rationale: Installing Python dependencies without caching to keep the image size small.
RUN pip install --no-cache-dir -r requirements.txt
# Rationale: Launching the Flask app using Gunicorn (a production-grade WSGI server) with 4 worker processes bound to port 7860.
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
