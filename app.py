from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
CORS(app)

TRANSLATE_API = "https://libretranslate.de/translate"

# Set up retry strategy
retry_strategy = Retry(
    total=3,  # Retry 3 times
    backoff_factor=1,  # Delay between retries (1, 2, 4, 8 seconds)
    status_forcelist=[500, 502, 503, 504],  # Retry on server errors (5xx)
    method_whitelist=["HEAD", "GET", "POST", "PUT", "DELETE"]  # Methods to retry
)
adapter = HTTPAdapter(max_retries=retry_strategy)

# Create a session and mount the adapter
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()

    if not data or 'text' not in data or 'target_lang' not in data:
        return jsonify({'error': 'Missing text or target language'}), 400

    text = data['text']
    target_lang = data['target_lang']
    
    payload = {
        'q': text,
        'source': 'auto',  # Automatically detect source language
        'target': target_lang,
        'format': 'text'
    }

    try:
        response = session.post(TRANSLATE_API, data=payload, timeout=10)  # Timeout after 10 seconds
        response.raise_for_status()  # Raise an exception for HTTP error codes (4xx, 5xx)
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. Please try again later.'}), 408
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    translated_text = response.json().get('translatedText', '')
    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
