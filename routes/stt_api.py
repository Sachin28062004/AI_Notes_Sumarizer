from flask import Blueprint, request, jsonify
from utils import speech_processor

stt_api = Blueprint('stt_api', __name__)

@stt_api.route('/stt/audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['file']
    try:
        text = speech_processor.process_audio(audio_file)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
