# Example: utils/deployment_tools.py
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the trained model
model = joblib.load('path/to/model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    prediction = model.predict([data['features']])
    return jsonify({'prediction': prediction.tolist()})

if __name__ == "__main__":
    app.run(debug=True)
