from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import io

router = APIRouter()

@router.post("/anomaly")
async def detect_anomalies(file: UploadFile = File(...)):
    content = await file.read()

    try:
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
    except Exception:
        return JSONResponse(content={"error": "Invalid CSV format."}, status_code=400)

    if df.empty or df.shape[1] < 2:
        return JSONResponse(content={"error": "File must contain at least 2 columns."}, status_code=400)

    values = df.iloc[:, 1]
    mean = values.mean()
    std = values.std()

    high = df[values > mean + 2 * std]
    low = df[values < mean - 2 * std]
    anomalies = pd.concat([high, low])

    if anomalies.empty:
        return JSONResponse(content={"message": "✅ No anomalies detected."})

    return JSONResponse(content={"anomalies": anomalies.to_dict(orient="records")})
