# utils/ocr.py
import pytesseract
from PIL import Image
import re

def extract_details(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    result = {}

    aadhaar_match = re.search(r"\d{4}\s\d{4}\s\d{4}", text)
    dob_match = re.search(r"\d{2}/\d{2}/\d{4}", text)
    gender = "Male" if "MALE" in text.upper() else "Female" if "FEMALE" in text.upper() else "Unknown"

    result["aadhaar_number"] = aadhaar_match.group() if aadhaar_match else None
    result["dob"] = dob_match.group() if dob_match else None
    result["gender"] = gender

    name_match = re.findall(r"(?<=\n)[A-Z][a-z]+\s[A-Z][a-z]+", text)
    result["name"] = name_match[0] if name_match else None

    return result
