import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

def load_and_train_model():
    df = pd.read_excel("app/data/updated_loans_data.xlsx", engine="openpyxl")

    df = df.drop(columns=["loan_id"], errors="ignore")

    # Label encode
    encoders = {
        "education": LabelEncoder(),
        "self_employed": LabelEncoder(),
        "loan_status": LabelEncoder(),
        "customer_rating": LabelEncoder(),
        "loan_type": LabelEncoder()
    }

    for col in encoders:
        df[col] = encoders[col].fit_transform(df[col].astype(str).str.strip().str.lower())

    # Optional: fillna for any missing collateral data
    df["present_gold_value"] = df.get("present_gold_value", 0)
    df["chit_paid_amount"] = df.get("chit_paid_amount", 0)

    X = df.drop("loan_status", axis=1)
    y = df["loan_status"]

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    return model, encoders


def predict_loan(model, encoders, input_data: dict):
    df = pd.DataFrame([input_data])
    for col in ["education", "self_employed", "customer_rating", "loan_type"]:
        df[col] = encoders[col].transform(df[col].astype(str).str.strip().str.lower())

    prediction = model.predict(df)[0]
    return encoders["loan_status"].inverse_transform([prediction])[0]