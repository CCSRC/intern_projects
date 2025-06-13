import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

from app.schemas import Transaction  # Ensure this does not cause circular import

# Load .env from project root dynamically (cross-platform)
from pathlib import Path
from dotenv import load_dotenv


import os

# Fix the .env path — adjust according to actual folder
env_path = Path("C:/Users/JOYAL JOSEPH/OneDrive/Desktop/fraud_detect_proj/.env")
load_dotenv(dotenv_path=env_path)


# Fetch environment variables
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Sanity check
if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
    raise ValueError("❌ One or more email environment variables are not set.")

def send_fraud_alert_email(cust_id: str, txn: Transaction, probability: float):
    print(f"[DEBUG] Preparing to send fraud alert email for customer {cust_id}")

    subject = f"⚠️ Fraudulent Transaction Detected for Customer {cust_id}"
    body = f"""
    A fraudulent transaction has been detected.

    Customer ID: {cust_id}
    Amount: {txn.amount}
    Transaction Type: {txn.transaction_type}
    Location: {txn.location}
    Device: {txn.device}
    Merchant: {txn.merchant}
    Time: {txn.timestamp}

    Fraud Probability: {probability:.2f}
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"[INFO] ✅ Email successfully sent to {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"[ERROR] ❌ Failed to send email: {e}")

# Optional: For debugging
if __name__ == "__main__":
    print(f"[DEBUG] Sender: {EMAIL_SENDER}")
    print(f"[DEBUG] Password: {'SET' if EMAIL_PASSWORD else 'NOT SET'}")
    print(f"[DEBUG] Receiver: {EMAIL_RECEIVER}")
