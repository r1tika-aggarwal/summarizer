import os
import pyaudio
import wave
import assemblyai as aai
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

# Constants
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")
aai.settings.api_key = ASSEMBLY_API_KEY

# Load the model and tokenizer once
model = AutoModelForSeq2SeqLM.from_pretrained("../fine_tuned_t5_final")
tokenizer = AutoTokenizer.from_pretrained("../fine_tuned_t5_final")


def record_audio(output_path="input.wav", duration_seconds=30):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=FRAMES_PER_BUFFER)
    frames = []

    for _ in range(0, int(RATE / FRAMES_PER_BUFFER * duration_seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(output_path, "wb") as obj:
        obj.setnchannels(CHANNELS)
        obj.setsampwidth(p.get_sample_size(FORMAT))
        obj.setframerate(RATE)
        obj.writeframes(b"".join(frames))


def transcribe_audio(file_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)
    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")
    return transcript.text


def summarize_text(input_text, max_length=1500, min_length=20, num_beams=4):
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", truncation=True)
    outputs = model.generate(
        inputs,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=num_beams,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def text_to_audio_gtts(text, output_file="summary.mp3", lang="en"):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_file)
