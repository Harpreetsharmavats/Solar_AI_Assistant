from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from utils.image_analysis import analyze_rooftop
from utils.roi_calculator import calculate_roi
import numpy as np
import io
import cv2
import os
from dotenv import load_dotenv
import traceback

import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🚀 Solar AI Assistant API is Live!"}

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if not contents:
            raise ValueError("Uploaded file is empty.")

        image_pil = Image.open(io.BytesIO(contents)).convert("RGB")
        image_np = np.array(image_pil)
        image_cv2 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        rooftop_data = analyze_rooftop(image_cv2)
        roi_data = calculate_roi(rooftop_data)

        return {
            "label": "rooftop",
            "confidence": 0.95,
            "rooftopData": rooftop_data,
            "roiData": roi_data
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post("/generate-report/")
async def generate_report(area: float = Form(...)):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing Gemini API Key")

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-pro")
        prompt = (
            f"You are a solar advisor. Based on a rooftop area of {area} m², generate a report including:\n"
            "- Estimated number of solar panels\n"
            "- Expected energy output (kWh/month)\n"
            "- Installation cost estimate\n"
            "- ROI duration\n"
            "- Recommended panel type"
        )

        response = model.generate_content(prompt)

        return {"report": response.text}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
