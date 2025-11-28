import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify
import numpy as np

# --------- CONFIG ----------
MODEL_PATH = "model.pkl"
CSV_PATH = "cleaned_data.csv"

# --------- APP ----------
app = Flask(__name__)

# Load model once
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Load dataset to get dropdown options (categorical values)
df = pd.read_csv(CSV_PATH)

# Define which columns are dropdown (categorical) and which are numeric text inputs
DROPDOWNS = ["year", "month", "day", "day_of_week"]  # show as dropdowns
NUMERIC_FIELDS = ["open", "high", "low", "volume"]  # text/number boxes

# Precompute unique sorted options for dropdowns
dropdown_options = {}
for col in DROPDOWNS:
    # convert to strings for safe HTML display, but keep numeric values for prediction
    vals = sorted(df[col].dropna().unique().astype(int).tolist())
    dropdown_options[col] = vals

@app.route("/")
def index():
    # send options to template
    return render_template(
        "index.html",
        dropdown_options=dropdown_options,
        numeric_fields=NUMERIC_FIELDS,
    )

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        # Extract values in the required order used in training:
        # ['open','high','low','volume','year','month','day','day_of_week']
        x_order = ["open","high","low","volume","year","month","day","day_of_week"]
        x_vals = []
        for key in x_order:
            if key not in data:
                return jsonify({"error": f"Missing key: {key}"}), 400
            # convert numeric strings to appropriate type (float or int)
            val = data[key]
            # volume may be large integer, open/high/low float
            if key in ["open","high","low"]:
                x_vals.append(float(val))
            else:
                # year/month/day/day_of_week/volume -> integers
                x_vals.append(int(val))

        X = np.array([x_vals])  # shape (1, n_features)
        pred = model.predict(X)
        # if model returns array
        predicted_close = float(pred[0])

        return jsonify({"predicted_close": round(predicted_close, 4)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
