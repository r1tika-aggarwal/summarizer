# Audio Summarizer Web App
A web application that lets users record or upload audio, automatically transcribes it using AssemblyAI, generates a concise summary using a fine-tuned T5 model, and can optionally convert the summary back to audio using gTTS for easy playback.

## Features
- Record audio or upload `.wav`, `.mp3` files
- Transcribe audio using AssemblyAI API
- Summarize long transcripts using a fine-tuned T5 model
- Convert the summary to audio using Google Text-to-Speech (gTTS)
- Clean and responsive web interface using Flask

## File Structure

| File / Folder           | Description |
|-------------------------|-------------|
| `app.py`                | Main Flask application to serve the web app |
| `final_logic.py`        | Core logic for transcription, summarization, and audio generation |
| `static/`               | Contains CSS and static assets |
| `templates/`            | Contains `index.html` for rendering UI |
| `cleaned_data.csv`      | Preprocessed text data used for model training |
| `newsdataset.ipynb`     | Notebook that processes raw data into `cleaned_data.csv` |
| `newsfinetune.ipynb`    | Notebook that fine-tunes the T5 model using `cleaned_data.csv` |
| `final.ipynb`           | End-to-end pipeline: record → transcribe → summarize → audio |
| `.gitignore`            | Ignores unnecessary or sensitive files |
| `README.md`             | Project overview and instructions |

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/r1tika-aggarwal/summarizer.git
cd audio-summarizer
```

2. **Install dependencies**

pip install flask pyaudio wave gtts transformers torch assemblyai python-dotenv

3. **Set your environment variable**

Create a `.env` file in the root directory and add:

```
ASSEMBLYAI_API_KEY=your_api_key_here
```

4. **Run the application**
python app.py
Visit `http://127.0.0.1:5000` in your browser.

## Notes
- Make sure your microphone is connected if you're using the recording feature.
- Replace `"../fine_tuned_t5_final"` with the path to your trained model directory.
- Summary audio output will be saved as `test_output1.mp3`.
