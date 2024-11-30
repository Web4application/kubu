from fastai.vision.all import *

def classify_image(image_path):
learn = load_learner('kubu-hai.h5')
img = PILImage.create(image_path)
pred, _, probs = learn.predict(img)
return pred, probs

if __name__ == "__main__":
image_path = 'path_to_your_image.jpg'
prediction, probabilities = classify_image(image_path)
print(f"Prediction: {prediction}, Probabilities: {probabilities}")
