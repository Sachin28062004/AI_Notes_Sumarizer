from flask import Blueprint, request, jsonify
from utils import ocr

ocr_api = Blueprint('ocr_api', __name__)

@ocr_api.route('/ocr/image', methods=['POST'])
def ocr_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    text = ocr.process_image(file)
    return jsonify({'text': text})

@ocr_api.route('/ocr/pdf', methods=['POST'])
def ocr_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    text = ocr.process_pdf(file)
    return jsonify({'text': text})
