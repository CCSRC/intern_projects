from fastapi import FastAPI
from pydantic import BaseModel
from app.model import load_and_train_model, predict_loan
from app.explainer.explain import explain_prediction

app = FastAPI(title="Loan Approval API")

model, label_encoder = load_and_train_model()

class LoanInput(BaseModel):
    no_of_dependents: int
    education: str
    self_employed: str
    income_annum: int
    loan_amount: int
    loan_term: int
    cibil_score: int
    residential_assets_value: int
    commercial_assets_value: int
    luxury_assets_value: int
    bank_asset_value: int
    customer_rating: str
    loan_type: str
    present_gold_value: float 
    collateral_value: float
    chit_or_fd_receipt_value: float



from app.explainer.explain import explain_prediction

@app.post("/predict_with_explanation")
def predict_with_explanation(input: LoanInput):
    input_data = input.dict()

    validation_result = validate_loan_constraints(input_data)
    if validation_result != "Approved":
        return {

            "loan_status": "Rejected",
            "reason": validation_result
        }

    loan_status = predict_loan(model, label_encoder, input_data)
    explanation = explain_prediction(input_data,loan_status)

    return {
        "loan_status": loan_status,
        "explanation": explanation
    }


def validate_loan_constraints(input_data: dict) -> str:
    loan_type = input_data["loan_type"].strip().lower()
    loan_amount = input_data["loan_amount"]

    if loan_type == "gold loan":
        present_gold_value = input_data.get("present_gold_value", 0.0)
        max_loan = 0.9 * present_gold_value

        max_loan = 0.9 * present_gold_value
        if loan_amount > max_loan:
            return (
            f"Rejected: Loan exceeds 90% of gold value "
            f"(loan amount: ₹{loan_amount}, gold value: ₹{present_gold_value:.0f}, max allowed: ₹{max_loan:.0f})"
        )

    elif loan_type == "secured loan":
        fd_value = input_data.get("bank_asset_value", 0)
        chit_paid = input_data.get("fd_receipt_value", 0)

        max_fd_loan = 0.95 * fd_value
        max_chit_loan = 0.8 * chit_paid
        total_max = max_fd_loan + max_chit_loan

        if loan_amount > total_max:
            return (
                f"Rejected: Loan exceeds collateral value "
                f"(FD max: ₹{max_fd_loan:.0f}, Chit max: ₹{max_chit_loan:.0f})"
            )

    elif loan_type == "staged loan":
        max_loan = 0.8 * input_data.get("collateral_value", 0)
        if loan_amount > max_loan:
            return "Rejected: Staged loan exceeds 80% of residential asset value."

    
    return "Approved"