import keras
import keras2onnx
import onnx

# Load your model
model = keras.models.load_model("kubu_hai_model.h5")

# Convert to ONNX
onnx_model = keras2onnx.convert_keras(model, model.name)

# Save ONNX model
onnx.save_model(onnx_model, "kubu_hai_model.onnx")
