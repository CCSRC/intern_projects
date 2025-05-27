# api/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from utils.classify import is_aadhar_image
from utils.ocr import extract_details

app = FastAPI()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = {"is_aadhar": False, "details": {}}

    if is_aadhar_image(file_location):
        result["is_aadhar"] = True
        result["details"] = extract_details(file_location)

    os.remove(file_location)
    return JSONResponse(content=result)
