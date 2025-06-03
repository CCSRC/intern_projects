import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from app.schemas import Transaction  # Avoid circular imports

load_dotenv()
from dotenv import load_dotenv
load_dotenv(dotenv_path="C:/Users/JOYAL JOSEPH/OneDrive/Desktop/fraud_detection_project/.env")



EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Sanity check for environment variables
if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
    raise ValueError("❌ One or more email environment variables are not set.")

def send_fraud_alert_email(cust_id, txn: Transaction, probability: float):
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
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        #server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[INFO] ✅ Email successfully sent to {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"[ERROR] ❌ Failed to send email: {e}")

print(f"[DEBUG] Using sender: {EMAIL_SENDER}, receiver: {EMAIL_RECEIVER}")

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="C:/Users/JOYAL JOSEPH/OneDrive/Desktop/fraud_detection_project/.env")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

print(f"[DEBUG] Sender: {EMAIL_SENDER}")
print(f"[DEBUG] Password: {'SET' if EMAIL_PASSWORD else 'NOT SET'}")
print(f"[DEBUG] Receiver: {EMAIL_RECEIVER}")
