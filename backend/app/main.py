from fastapi import FastAPI
from pydantic import BaseModel
from train.ensemble_prep import ensemble_predict

app = FastAPI()

class Input(BaseModel):
    rainfall_mm: float
    temp_C: float
    slope_angle: float
    vibration: float
    displacement: float
    pore_pressure: float

@app.post("/predict")
def predict(inp: Input):
    result = ensemble_predict(inp.dict())
    return result

@app.get("/")
def root():
    return {"message": "✅ Rockfall Prediction API is running!"}
