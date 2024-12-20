import os
import joblib
from flask import Flask, request, jsonify
from prometheus_client import Counter, start_http_server, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

app = Flask(__name__)

# Load the model locally
MODEL_PATH = os.environ.get("MODEL_PATH", "/app/model/model.pkl")

model = joblib.load(MODEL_PATH)

# Custom Prometheus metrics
prediction_counter = Counter('prediction_requests', 'Number of prediction requests')
error_counter = Counter('prediction_errors', 'Number of prediction errors')

@app.route('/')
def welcome():
    return "Welcome to the LightGBM Classification API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = data['features']

        # Ensure the input is a 2D array (even for single predictions)
        if not isinstance(features[0], list):
            features = [features]

        predictions = model.predict(features)
        prediction_counter.inc()  # Increment prediction counter
        return jsonify({'predictions': predictions.tolist()})
    except Exception as e:
        error_counter.inc()  # Increment error counter
        return jsonify({'error': str(e)}), 500

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    start_http_server(5002)  # Start Prometheus metrics server
    app.run(host='0.0.0.0', port=5001)

