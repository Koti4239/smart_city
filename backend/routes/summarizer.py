from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import requests

router = APIRouter()

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_TOKEN = "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"  # 🔁 Replace with your Hugging Face token

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@router.post("/summarize")
async def summarize_policy(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")

    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        result = response.json()

        # ✅ Model loading or error message
        if "error" in result:
            return JSONResponse(status_code=503, content={"error": result["error"]})

        # ✅ Success summary
        if isinstance(result, list) and "summary_text" in result[0]:
            return JSONResponse(content={"summary": result[0]["summary_text"]})

        return JSONResponse(status_code=500, content={"error": "Unexpected response", "raw": result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "raw": response.text})
