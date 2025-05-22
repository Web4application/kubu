from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
data = request.get_json()
# Perform prediction using your model
result = {"prediction": "example_result"}
return jsonify(result)

if __name__ == '__main__':
app.run(host='127.0.0.1', port=5000)
