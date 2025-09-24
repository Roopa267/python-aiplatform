from flask import Flask, request, jsonify
from google.cloud import aiplatform

app = Flask(__name__)

# ✅ Replace these with your actual values (already given)
PROJECT_ID = "569713108976"
REGION = "us-central1"
ENDPOINT_ID = "1010876696926093312"

# Initialize AI Platform client
client = aiplatform.gapic.PredictionServiceClient()
endpoint = f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"

@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON payload like:
    {
        "instances": [
            {
                "hr_bpm": 80,
                "spo2_pct": 95,
                "bp_sys_mean": 120,
                "bp_dia_mean": 80,
                "rr_mean": 16,
                "temp_mean": 36.8
            }
        ]
    }
    """
    try:
        input_data = request.json.get("instances", [])
        if not input_data:
            return jsonify({"error": "No instances provided"}), 400

        response = client.predict(endpoint=endpoint, instances=input_data)
        return jsonify({"predictions": response.predictions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))  # Cloud Run requires this
    app.run(host="0.0.0.0", port=port)
