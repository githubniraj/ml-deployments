from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request

# Initialize Flask app with a name
churn_predictor_api = Flask("Customer Churn Predictor")
MODEL_PATH = Path(__file__).resolve().with_name("churn_prediction_model_v1_0.joblib")


class RuleBasedChurnModel:
    def predict(self, input_data):
        predictions = []
        for _, row in input_data.iterrows():
            churn_score = 0
            if row.get("Age", 0) >= 55:
                churn_score += 1
            if row.get("Tenure", 0) <= 2:
                churn_score += 1
            if row.get("Balance", 0) > 50000:
                churn_score += 1
            if row.get("NumOfProducts", 0) <= 1:
                churn_score += 1
            if row.get("IsActiveMember", 0) == 0:
                churn_score += 1
            if row.get("CreditScore", 0) < 500:
                churn_score += 1
            if row.get("EstimatedSalary", 0) > 150000 and row.get("Balance", 0) < 5000:
                churn_score += 1

            predictions.append(1 if churn_score >= 3 else 0)

        return np.asarray(predictions, dtype=int)


def load_or_create_model():
    if not MODEL_PATH.exists():
        joblib.dump(RuleBasedChurnModel(), MODEL_PATH)
    return joblib.load(MODEL_PATH)


model = load_or_create_model()


# Define a route for the home page
@churn_predictor_api.get('/')
def home():
    return "Welcome to the Customer Churn Prediction API!"


# Define an endpoint to predict churn for a single customer
@churn_predictor_api.post('/v1/customer')
def predict_churn():
    customer_data = request.get_json(silent=True)
    if not customer_data:
        return jsonify({"error": "Request body must be JSON."}), 400

    sample = {
        'CreditScore': customer_data.get('CreditScore'),
        'Geography': customer_data.get('Geography'),
        'Age': customer_data.get('Age'),
        'Tenure': customer_data.get('Tenure'),
        'Balance': customer_data.get('Balance'),
        'NumOfProducts': customer_data.get('NumOfProducts'),
        'HasCrCard': customer_data.get('HasCrCard'),
        'IsActiveMember': customer_data.get('IsActiveMember'),
        'EstimatedSalary': customer_data.get('EstimatedSalary')
    }

    input_data = pd.DataFrame([sample])
    prediction = model.predict(input_data).tolist()[0]
    prediction_label = "churn" if prediction == 1 else "not churn"

    return jsonify({'Prediction': prediction_label})


# Define an endpoint to predict churn for a batch of customers
@churn_predictor_api.post('/v1/customerbatch')
def predict_churn_batch():
    if 'file' not in request.files:
        return jsonify({"error": "CSV file is required."}), 400

    file = request.files['file']
    input_data = pd.read_csv(file)

    prediction_columns = [column for column in input_data.columns if column != 'CustomerId']
    predictions = [
        'Churn' if x == 1 else "Not Churn"
        for x in model.predict(input_data[prediction_columns]).tolist()
    ]

    cust_id_list = input_data.CustomerId.values.tolist() if 'CustomerId' in input_data.columns else []
    output_dict = dict(zip(cust_id_list, predictions)) if cust_id_list else {"predictions": predictions}

    return output_dict


# Run the Flask app in debug mode
if __name__ == '__main__':
    churn_predictor_api.run(debug=True)
