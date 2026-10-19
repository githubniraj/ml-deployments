#!/bin/bash

echo "🚀 Starting Backend (Flask)..."
cd backend_files
pip install -r requirements.txt
python app.py &

echo "🚀 Starting Frontend (Streamlit)..."
cd ../frontend_files
pip install -r requirements.txt
streamlit run app.py --server.port 8501
