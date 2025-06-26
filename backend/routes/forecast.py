from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from sklearn.linear_model import LinearRegression
import io

router = APIRouter()

@router.post("/forecast")
async def forecast_kpi(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        if df.shape[1] < 2:
            raise HTTPException(status_code=400, detail="CSV must have at least two columns.")
        x = df.iloc[:, 0].values.reshape(-1, 1)
        y = df.iloc[:, 1].values
        model = LinearRegression().fit(x, y)
        next_x = [[x[-1][0] + 1]]
        forecast_value = model.predict(next_x)[0]
        return {"forecast": round(float(forecast_value), 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during forecasting: {str(e)}")