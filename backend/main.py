from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import summarizer, forecast, anomaly
from routes.anomaly import router # ✅ correct

 # Make sure this matches your filename

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summarizer.router)
app.include_router(forecast.router)
app.include_router(anomaly.router)

@app.get("/")
def read_root():
    return {"message": "Smart City Assistant Backend"}
app.include_router(router)
