from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # To handle cross-origin requests from the React frontend

app = Flask(__name__)
CORS(app)  # Enable CORS

# LibreTranslate API endpoint
TRANSLATE_API = "https://libretranslate.de/translate"

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()

    # Check if 'text' and 'target_lang' are in the request
    if not data or 'text' not in data or 'target_lang' not in data:
        return jsonify({'error': 'Missing text or target language'}), 400

    text = data['text']
    target_lang = data['target_lang']
    
    # Translate text
    payload = {
        'q': text,
        'source': 'auto',  # Automatically detect source language
        'target': target_lang,
        'format': 'text'
    }
    response = requests.post(TRANSLATE_API, data=payload)
    
    if response.status_code != 200:
        return jsonify({'error': 'Translation failed'}), 500
    
    translated_text = response.json().get('translatedText', '')

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
