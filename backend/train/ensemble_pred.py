import joblib
import numpy as np
import shap
import pandas as pd

# Load trained model + scaler
xgb_model = joblib.load("../app/models/xgb_model.pkl")
scaler = joblib.load("../app/models/scaler.pkl")

# Define feature names (same as training)
FEATURE_NAMES = ["rainfall_mm", "temp_C", "slope_angle", "vibration", "displacement", "pore_pressure"]

# Create SHAP explainer
explainer = shap.TreeExplainer(xgb_model)


def shap_explain(input_dict):
    """Generate SHAP explanations for top 3 features."""
    x = pd.DataFrame([[
        input_dict["rainfall_mm"],
        input_dict["temp_C"],
        input_dict["slope_angle"],
        input_dict["vibration"],
        input_dict["displacement"],
        input_dict["pore_pressure"]
    ]], columns=FEATURE_NAMES)

    x_scaled = scaler.transform(x)
    shap_values = explainer.shap_values(x_scaled)

    mean_abs_vals = np.abs(shap_values).flatten()
    sorted_idx = np.argsort(mean_abs_vals)[::-1]

    top_reasons = []
    for idx in sorted_idx[:3]:
        feature_name = FEATURE_NAMES[idx]
        impact = shap_values[0][idx]
        sign = "↑" if impact > 0 else "↓"
        top_reasons.append(f"{feature_name} {sign} ({impact:.2f})")

    return top_reasons


def ensemble_predict(input_dict):
    """Run prediction using XGBoost only (for now)."""
    X = np.array([[
        input_dict["rainfall_mm"],
        input_dict["temp_C"],
        input_dict["slope_angle"],
        input_dict["vibration"],
        input_dict["displacement"],
        input_dict["pore_pressure"]
    ]])
    X_scaled = scaler.transform(X)

    proba = xgb_model.predict_proba(X_scaled)[0]
    pred = np.argmax(proba)
    risk_score = float(proba[pred])

    if pred == 0:
        level = "Green"
    elif pred == 1:
        level = "Yellow"
    else:
        level = "Red"

    reasons = shap_explain(input_dict)

    return {
        "risk_score": round(risk_score * 100, 1),
        "risk_level": level,
        "proba": [round(float(p), 3) for p in proba],
        "reasons": reasons
    }


# Quick test
if __name__ == "__main__":
    dummy_input = {
        "rainfall_mm": 120,
        "temp_C": 25,
        "slope_angle": 38,
        "vibration": 0.4,
        "displacement": 0.6,
        "pore_pressure": 3.2,
    }
    result = ensemble_predict(dummy_input)
    print(result)
