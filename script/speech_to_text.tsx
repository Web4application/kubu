from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torch
import soundfile as sf

# Load pre-trained model and tokenizer
tokenizer = Wav2Vec2Tokenizer.from_pretrained("enoch/llama-65b-hf")
model = Wav2Vec2ForCTC.from_pretrained("enoch/llama-65b-hf")

# Load audio file
speech, rate = sf.read("roda.wav")

# Tokenize and predict
input_values = tokenizer(speech, return_tensors="pt").input_values
logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)

# Decode the prediction
transcription = tokenizer.decode(predicted_ids[0])
print(transcription)
