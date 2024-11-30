from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torch
import soundfile as sf

# Load pre-trained model and tokenizer
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# Load audio file
speech, rate = sf.read("kubu-hai/music/roda.wav")

# Tokenize and predict
input_values = tokenizer(speech, return_tensors="pt").input_values
logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)

# Decode the prediction
transcription = tokenizer.decode(predicted_ids[0])
print(transcription)
