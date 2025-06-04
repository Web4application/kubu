from fastapi import FastAPI, UploadFile, File
import onnxruntime as ort
import numpy as np
from PIL import Image
import io

app = FastAPI()
session = ort.InferenceSession("kubu_hai_model.onnx")

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).resize((224, 224))
    input_array = np.array(image) / 255.0
    input_array = input_array.astype(np.float32).reshape(1, 224, 224, 3)

    inputs = {session.get_inputs()[0].name: input_array}
    output = session.run(None, inputs)
    
    return {"prediction": output[0].tolist()}
