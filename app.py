from flask import Flask, render_template, request, jsonify
import os
import requests
from werkzeug.utils import secure_filename
from faster_whisper import WhisperModel

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model (base = fast, low RAM)
model = WhisperModel("base", compute_type="int8")  # use "int8" for minimal CPU load

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['audio']
    lang = request.form['lang']

    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(filepath)

    text = transcribe(filepath)
    translated_text = translate_text(text, lang)

    return jsonify({'translated_text': translated_text})

def transcribe(filepath):
    segments, _ = model.transcribe(filepath)
    return " ".join([seg.text for seg in segments])

def translate_text(text, target_lang):
    response = requests.post("https://libretranslate.de/translate", json={
        "q": text,
        "source": "en",
        "target": target_lang,
        "format": "text"
    }, headers={"Content-Type": "application/json"})
    
    return response.json()['translatedText']

if __name__ == "__main__":
    app.run(debug=True)
