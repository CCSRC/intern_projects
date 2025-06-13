from fastapi import FastAPI, HTTPException
from app.schemas import Transaction
import pandas as pd
import shap
import os
from datetime import datetime
from dotenv import load_dotenv

from app.utils.email_alert import send_fraud_alert_email
from app.model.trainer import load_and_train_models, preprocess

# Load environment variables from app/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI()

# Load customer data and LightGBM models at startup
customer_dfs, models, X_data = load_and_train_models()

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running"}

@app.post("/predict/{cust_id}")
def predict(cust_id: str, txn: Transaction):
    if cust_id not in models:
        raise HTTPException(status_code=404, detail=f"Model for customer {cust_id} not found.")

    # Convert input data to dict and parse timestamp
    input_dict = txn.dict()
    try:
        input_dict['timestamp'] = pd.Timestamp(input_dict['timestamp'])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timestamp format.")

    # Prepare test data
    df = customer_dfs[cust_id]
    test_df = df.tail(1).copy()
    for key, val in input_dict.items():
        test_df[key] = val

    X, _, _ = preprocess(test_df)
    x_input = X.tail(1)

    # Get model and make prediction
    model = models[cust_id]
    pred = int(model.predict(x_input)[0])
    prob = float(model.predict_proba(x_input)[0][1]) if hasattr(model, 'predict_proba') else float(pred)

    # Get SHAP values
    explainer = shap.Explainer(model)
    shap_values = explainer(x_input)
    shap_contributions = dict(zip(x_input.columns, shap_values.values[0].tolist()))

    # Trigger fraud alert if needed
    if pred == 1:
        print(f"[DEBUG] 🚨 FRAUD detected for customer {cust_id} with probability {prob:.4f}")
        send_fraud_alert_email(cust_id, txn, prob)

    # Return response
    return {
        "prediction": "FRAUD" if pred == 1 else "LEGITIMATE",
        "probability": prob,
        "feature_contributions": shap_contributions
    }
