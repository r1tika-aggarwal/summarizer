# app.py
from flask import Flask, render_template, request, send_from_directory
import os
from final_logic import transcribe_audio, summarize_text,text_to_audio_gtts

UPLOAD_FOLDER = 'uploads'
AUDIO_OUTPUT_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    transcript = ""
    audio_filename = ""
    if request.method == 'POST':
        if 'audio' not in request.files:
            return render_template('index.html', error="No file part")
        file = request.files['audio']
        if file.filename == '':
            return render_template('index.html', error="No selected file")
        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            try:
                transcript = transcribe_audio(file_path)
                summary = summarize_text(transcript)
                
                # Convert summary to audio
                audio_filename = "summary_audio.mp3"
                audio_path = os.path.join(AUDIO_OUTPUT_FOLDER, audio_filename)
                text_to_audio_gtts(summary, output_file=audio_path)
                
            except Exception as e:
                return render_template('index.html', error=f"Error: {str(e)}")
    return render_template('index.html', summary=summary, transcript=transcript,audio_file=audio_filename)

@app.route('/static/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
