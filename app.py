from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from utils.image_analysis import analyze_rooftop
from utils.roi_calculator import calculate_roi
import openai
import numpy as np
import io
import cv2
import os
from dotenv import load_dotenv
import traceback
from fastapi import Form

# Load environment variables (works locally)
load_dotenv()

# Load OpenAI API Key from environment (works on Railway too)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict origins
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

        # Convert to PIL image
        image_pil = Image.open(io.BytesIO(contents)).convert("RGB")

        # Convert PIL to OpenCV
        image_np = np.array(image_pil)
        image_cv2 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Analyze rooftop
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
    try:
        prompt = (
            f"You are a solar advisor. Based on a rooftop area of {area} m², generate a report including:\n"
            "- Estimated number of solar panels\n"
            "- Expected energy output (kWh/month)\n"
            "- Installation cost estimate\n"
            "- ROI duration\n"
            "- Recommended panel type"
        )

        # ✅ Fix for OpenAI v1.x SDK
        client = openai.OpenAI(api_key=openai.api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a solar advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        return {"report": response.choices[0].message.content}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

