# Rationale: Builds the Streamlit frontend. Uses a slim Python base, installs the specific Streamlit UI dependencies, and starts the web server on port 8501.
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
