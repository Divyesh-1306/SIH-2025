from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from train.ensemble_pred import ensemble_predict

app = FastAPI(title="Rockfall Prediction API")

# Enable CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/sample_cases")
def sample_cases():
    safe = {
        "rainfall_mm": 5,
        "temp_C": 22,
        "slope_angle": 20,
        "vibration": 0.05,
        "displacement": 0.1,
        "pore_pressure": 0.5,
    }
    caution = {
        "rainfall_mm": 45,
        "temp_C": 28,
        "slope_angle": 32,
        "vibration": 0.25,
        "displacement": 0.6,
        "pore_pressure": 1.8,
    }
    high = {
        "rainfall_mm": 120,
        "temp_C": 30,
        "slope_angle": 40,
        "vibration": 0.6,
        "displacement": 1.5,
        "pore_pressure": 3.5,
    }
    return {
        "safe": safe,
        "caution": caution,
        "high": high,
    }


@app.get("/")
def root():
    return {"message": "✅ Rockfall Prediction API is running!"}
