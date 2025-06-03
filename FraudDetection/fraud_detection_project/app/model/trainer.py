import os
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Store customer data, models, and feature data
customer_dfs = {}
models = {}
X_data = {}

# Preprocessing function to process and prepare features
def preprocess(df):
    df = df.copy()
    
    # Extract hour and day of the week from the timestamp
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek

    # Apply label encoding to categorical columns
    label_cols = ['transaction_type', 'location', 'device', 'merchant']
    for col in label_cols:
        df[col] = LabelEncoder().fit_transform(df[col])

    # Select features and target column
    features = ['amount', 'transaction_type', 'location', 'device', 'merchant', 'hour', 'day_of_week']
    X = df[features]
    y = df['is_fraud']  # Target column
    return X, y, df

# Function to load data and train models for each customer
def load_and_train_models():
    path = "app/data/customers_data"
    
    # Load data for each customer
    for file in os.listdir(path):
        if file.endswith(".csv"):
            cust_id = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(path, file), parse_dates=["timestamp"])
            customer_dfs[cust_id] = df

    # Train LightGBM models for each customer
    for cust_id, df in customer_dfs.items():
        X, y, _ = preprocess(df)

        # Skip customers with insufficient samples for each class
        if y.value_counts().min() < 2:
            print(f"[WARN] Skipping {cust_id}: Not enough class diversity")
            continue

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Initialize LightGBM model
        model = LGBMClassifier(random_state=42, boosting_type='gbdt', objective='binary', metric='binary_error')

        # Train the model
        model.fit(X_train, y_train)

        # Store the trained model and feature data
        models[cust_id] = model
        X_data[cust_id] = X

        # Optionally evaluate the model on test data (you could also save models or log metrics)
        y_pred = model.predict(X_test)
        accuracy = (y_pred == y_test).mean()
        print(f"[INFO] {cust_id} Model Accuracy: {accuracy * 100:.2f}%")

    return customer_dfs, models, X_data

