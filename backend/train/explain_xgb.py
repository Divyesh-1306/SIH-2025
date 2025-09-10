import joblib
import shap
import numpy as np
import pandas as pd
xgb_model = joblib.load("../app/models/xgb_model.pkl")
scaler = joblib.load("../app/models/scaler.pkl")
FEATURE_NAMES = ["rainfall_7d_sum", "slope_angle", "vibration", "displacement_trend", "pore_pressure"]
explainer = shap.TreeExplainer(xgb_model)

def shap_explain(input_dict):
    x = pd.DataFrame([[
        input_dict["rainfall_7d_sum"],
        input_dict["slope_angle"],
        input_dict["vibration"],
        input_dict["displacement_trend"],
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
if __name__ == "__main__":
    dummy_input = {
        "rainfall_7d_sum": 120,
        "slope_angle": 38,
        "vibration": 0.4,
        "displacement_trend": 0.3,
        "pore_pressure": 1.2,
    }
    reasons = shap_explain(dummy_input)
    print("Top risk factors:", reasons)
