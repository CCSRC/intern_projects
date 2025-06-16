def explain_prediction(input_data: dict, loan_status: str) -> str:
    reasons = []

    loan_amount = input_data.get("loan_amount", 0)
    gold_value = input_data.get("present_gold_value", 0)

    if loan_status.lower() == "rejected":
        return (
            f"Rejected: Loan exceeds 90% of gold value "
            f"(loan amount: ₹{loan_amount}, gold value: ₹{gold_value}, "
            f"max allowed: ₹{gold_value * 0.9:.0f})"
        )

    # Approval reasons
    if input_data["income_annum"] > 500000:
        reasons.append("your income is high")
    if input_data["cibil_score"] >= 750:
        reasons.append("your CIBIL score is excellent")
    if loan_amount < input_data["income_annum"] * 0.3:
        reasons.append("your loan amount is reasonable")
    if input_data["bank_asset_value"] + input_data["residential_assets_value"] > 500000:
        reasons.append("you own valuable assets")
    if input_data["self_employed"].strip().lower() == "no":
        reasons.append("you have a stable job")
    if input_data["loan_type"].strip().lower() == "gold loan":
        reasons.append("loan type is gold loan, which is often quickly approved with collateral")

    if not reasons:
        return "Your application was evaluated, but we could not find strong financial indicators."

    return (
        f"Your loan application was approved because "
        f"{', and '.join(reasons)}. "
        f"(loan amount: ₹{loan_amount}, gold value: ₹{gold_value})"
    )