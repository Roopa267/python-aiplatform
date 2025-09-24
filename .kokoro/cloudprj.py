from flask import Flask, request, jsonify
from google.cloud import aiplatform

app = Flask(__name__)

PROJECT_ID = "569713108976"
REGION = "us-central1"
ENDPOINT_ID = "1010876696926093312"

client = aiplatform.gapic.PredictionServiceClient()
endpoint = f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"

@app.route("/")
def home():
    return "Airway prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
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
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
