from fastapi import FastAPI, HTTPException
from app.schemas import Transaction
import pandas as pd
import shap
from datetime import datetime
import os

from app.utils.email_alert import send_fraud_alert_email
from app.model.trainer import load_and_train_models, preprocess

app = FastAPI()

customer_dfs, models, X_data = load_and_train_models()

@app.get("/")
def root():
    return {"message": "Fraud Detection API is running"}

@app.post("/predict/{cust_id}")
def predict(cust_id: str, txn: Transaction):
    if cust_id not in models:
        raise HTTPException(status_code=404, detail=f"Model for customer {cust_id} not found.")

    input_dict = txn.dict()
    input_dict['timestamp'] = pd.Timestamp(input_dict['timestamp'])

    df = customer_dfs[cust_id]
    test_df = df.tail(1).copy()
    for key, val in input_dict.items():
        test_df[key] = val

    X, _, _ = preprocess(test_df)
    x_input = X.tail(1)

    model = models[cust_id]
    pred = int(model.predict(x_input)[0])
    prob = float(model.predict_proba(x_input)[0][1])

    explainer = shap.Explainer(model)
    shap_values = explainer(x_input)
    shap_contributions = dict(zip(x_input.columns, shap_values.values[0].tolist()))

    if pred == 1:
        send_fraud_alert_email(cust_id, txn, prob)

    return {
        "prediction": "FRAUD" if pred == 1 else "LEGITIMATE",
        "probability": prob,
        "feature_contributions": shap_contributions
    }
