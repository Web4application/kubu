from fastapi import FastAPI, UploadFile, File
from fastai_model import classify_image

app = FastAPI()

@app.post("/classify-image/")
async def classify_image_endpoint(file: UploadFile = File(...)):
with open("temp.jpg", "wb") as buffer:
buffer.write(await file.read())
prediction, probabilities = classify_image("temp.jpg")
return {"prediction": str(prediction), "probabilities": probabilities.tolist()}
