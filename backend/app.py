from flask import Flask, request, jsonify, send_file
import requests
from flask_cors import CORS
import os
from pathlib import Path
import openai
import base64

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = 'YOUR API KEY'
openai.api_key = OPENAI_API_KEY

AUDIO_DIR = Path(__file__).parent / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

def translate_text(text, target_language):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'model': 'gpt-4',
        'messages': [
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
        ],
        'max_tokens': 1000,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({'error': 'Missing text'}), 400


    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'model': 'tts-1',
        'input': text,
        'voice': 'alloy',
    }

    response = requests.post('https://api.openai.com/v1/audio/speech', headers=headers, json=data, stream=True)
    
    if response.status_code == 200:
        # You may want to save the audio file and return its URL instead
        return jsonify({'audio_url': 'data:audio/mpeg;base64,' + base64.b64encode(response.content).decode('utf-8')})
    else:
        return jsonify({'error': f"Error: {response.status_code} - {response.text}"}), 500




@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language')

    if not text or not target_language:
        return jsonify({'error': 'Missing text or target_language'}), 400

    translated_text = translate_text(text, target_language)
    return jsonify({'translated_text': translated_text})

@app.route('/speech', methods=['POST'])
def speech():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'Missing text'}), 400

    file_path = text_to_speech(text, 'output.mp3')
    if file_path:
        return send_file(file_path, mimetype='audio/mpeg')
    else:
        return jsonify({'error': 'Failed to generate speech'}), 500

if __name__ == '__main__':
    app.run(debug=True)
