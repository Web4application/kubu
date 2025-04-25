import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from PIL import Image
from dataclasses import dataclass
from typing import Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ModelInfo:
    repo: str
    adapter: Optional[str] = None

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float32 if DEVICE == "cpu" else "auto"

# Define models for the application
class HealthcareModel(torch.nn.Module):
    def __init__(self):
        super(HealthcareModel, self).__init__()
        self.fc1 = torch.nn.Linear(10, 50)
        self.relu = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(50, 1)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.sigmoid(x)

class FinanceModel(torch.nn.Module):
    def __init__(self):
        super(FinanceModel, self).__init__()
        self.lstm = torch.nn.LSTM(input_size=10, hidden_size=50, num_layers=2, batch_first=True)
        self.fc = torch.nn.Linear(50, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Use the last output of the LSTM
        return out

class EducationModel(torch.nn.Module):
    def __init__(self):
        super(EducationModel, self).__init__()
        self.fc1 = torch.nn.Linear(10, 50)
        self.fc2 = torch.nn.Linear(50, 5)  # Output is a score range for grading

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.softmax(self.fc2(x), dim=1)
        return x

class EntertainmentModel(torch.nn.Module):
    def __init__(self):
        super(EntertainmentModel, self).__init__()
        self.fc1 = torch.nn.Linear(10, 50)
        self.fc2 = torch.nn.Linear(50, 10)  # Output multiple recommendations

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# Instantiate models
healthcare_model = HealthcareModel().to(DEVICE)
finance_model = FinanceModel().to(DEVICE)
education_model = EducationModel().to(DEVICE)
entertainment_model = EntertainmentModel().to(DEVICE)

# Flask app setup
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def preprocess_data(data, domain):
    logger.debug(f"Preprocessing data for {domain}")
    if domain == "healthcare":
        return torch.tensor(data).float().unsqueeze(0).to(DEVICE)  # Example normalization
    elif domain == "finance":
        return torch.tensor(data).float().unsqueeze(0).to(DEVICE)  # Example scaling
    elif domain == "education":
        return torch.tensor(data).float().unsqueeze(0).to(DEVICE)  # Example grading preprocessing
    elif domain == "entertainment":
        return torch.tensor(data).float().unsqueeze(0).to(DEVICE)  # Example preferences handling
    return None

@app.route('/healthcare/predict', methods=['POST'])
def healthcare_predict():
    try:
        data = preprocess_data(request.json['data'], "healthcare")
        result = healthcare_model(data)
        diagnosis = "Condition A" if result.item() > 0.5 else "Condition B"
        return jsonify({"prediction": diagnosis})
    except Exception as e:
        logger.exception("Error in healthcare prediction")
        return jsonify({"error": str(e)}), 500

@app.route('/finance/analyze', methods=['POST'])
def finance_analyze():
    try:
        data = preprocess_data(request.json['data'], "finance")
        result = finance_model(data)
        trend = "Increasing" if result.item() > 0 else "Decreasing"
        return jsonify({"prediction": trend})
    except Exception as e:
        logger.exception("Error in finance analysis")
        return jsonify({"error": str(e)}), 500

@app.route('/education/grade', methods=['POST'])
def education_grade():
    try:
        data = preprocess_data(request.json['data'], "education")
        result = education_model(data)
        grade = result.argmax(dim=1).item()
        return jsonify({"grade": grade})
    except Exception as e:
        logger.exception("Error in education grading")
        return jsonify({"error": str(e)}), 500

@app.route('/entertainment/recommend', methods=['POST'])
def entertainment_recommend():
    try:
        data = preprocess_data(request.json['data'], "entertainment")
        result = entertainment_model(data)
        recommendations = result.topk(k=5).indices.tolist()  # Top 5 recommendations
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        logger.exception("Error in entertainment recommendations")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
