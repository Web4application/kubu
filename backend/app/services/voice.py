import os
import whisper
from gtts import gTTS
from tempfile import NamedTemporaryFile

model = whisper.load_model("base")

def transcribe_audio(file):
    temp = NamedTemporaryFile(delete=False)
    temp.write(file.file.read())
    temp.close()
    result = model.transcribe(temp.name)
    return result["text"]

def synthesize_text(text: str) -> str:
    tts = gTTS(text=text)
    output_path = f"/tmp/audio_{hash(text)}.mp3"
    tts.save(output_path)
    return output_path
