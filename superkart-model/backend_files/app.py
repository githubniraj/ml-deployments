# Import necessary libraries
import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Rationale: Initializing the Flask application which acts as our backend web server.
superkart_api = Flask("SuperKart")

# Rationale: Loading the serialized XGBoost model globally so it's ready in memory when requests come in.
model = joblib.load("superkart_model.joblib")

# Rationale: Root endpoint acting as a health check to verify the API is running.
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart System"

# Rationale: POST endpoint designed to accept JSON data for a single product, parse it into a DataFrame, predict using the loaded model, and return the numerical prediction as JSON.
@superkart_api.post('/v1/predict')
def predict_sales():
    data = request.get_json()
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Product_Id_char': data['Product_Id_char'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type_Category': data['Product_Type_Category']
    }
    input_data = pd.DataFrame([sample])
    prediction = model.predict(input_data).tolist()[0]
    return jsonify({'Sales': float(prediction)})

# Rationale: Batch POST endpoint that accepts a multipart CSV file upload, reads it directly into Pandas, predicts across all rows efficiently, and returns a dictionary map of predictions.
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    file = request.files['file']
    input_data = pd.read_csv(file)
    predictions = model.predict(input_data).tolist()
    output_dict = {str(i): round(pred, 2) for i, pred in enumerate(predictions)}
    return output_dict

# Rationale: Runs the Flask app on host 0.0.0.0 making it accessible externally to the container.
if __name__ == '__main__':
    superkart_api.run(debug=True, host='0.0.0.0')
