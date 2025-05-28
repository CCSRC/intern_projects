import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

customer_dfs = {}
models = {}
X_data = {}

def preprocess(df):
    df = df.copy()
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    label_cols = ['transaction_type', 'location', 'device', 'merchant']
    for col in label_cols:
        df[col] = LabelEncoder().fit_transform(df[col])
    features = ['amount', 'transaction_type', 'location', 'device', 'merchant', 'hour', 'day_of_week']
    X = df[features]
    y = df['is_fraud']
    return X, y, df

def load_and_train_models():
    path = "app/data/customers_data"
    for file in os.listdir(path):
        if file.endswith(".csv"):
            cust_id = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(path, file), parse_dates=["timestamp"])
            customer_dfs[cust_id] = df

    for cust_id, df in customer_dfs.items():
        X, y, _ = preprocess(df)

        # Skip if not enough samples for each class
        if y.value_counts().min() < 2:
            print(f"[WARN] Skipping {cust_id}: Not enough class diversity")
            continue

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        model = xgb.XGBClassifier(eval_metric='logloss')
        model.fit(X_train, y_train)
        models[cust_id] = model
        X_data[cust_id] = X

    return customer_dfs, models, X_data
