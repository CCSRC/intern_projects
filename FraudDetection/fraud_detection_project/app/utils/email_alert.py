import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.main import Transaction

from dotenv import load_dotenv
load_dotenv()

import os
EMAIL_SENDER = os.getenv("EMAIL_SENDER")


EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_fraud_alert_email(cust_id, txn: Transaction, probability: float):
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
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[INFO] Email sent to {EMAIL_RECEIVER}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
