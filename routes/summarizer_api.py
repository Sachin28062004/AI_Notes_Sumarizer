from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import utils.summarizer as summarizer
import utils.mindmap as mindmap_generator
import utils.ocr as ocr_processor
import utils.speech_processor as speech_processor
import utils.ALLOWED_EXTENSIONS as ALLOWED_EXTENSIONS
import tempfile

summarizer_api = Blueprint('summarizer_api', __name__)


def allowed_file(filename, file_types):
    """Check if file extension is allowed."""
    extensions = set()
    for file_type in file_types:
        extensions.update(ALLOWED_EXTENSIONS.get(file_type, set()))
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@summarizer_api.route('/summarize-text', methods=['POST'])
def summarize_text():
    """Endpoint to summarize text input."""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    length = data.get('length', 'medium')  # short, medium, large
    output_format = data.get('format', 'paragraph')  # paragraph, bullets, mindmap
    
    if output_format == 'mindmap':
        result = mindmap_generator.generate_mindmap(text)
    else:
        result = summarizer.summarize(text, length, output_format)
    
    return jsonify({'summary': result})

@summarizer_api.route('/upload-document', methods=['POST'])
def upload_document():
    """Endpoint to upload and process documents."""
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # Process file if allowed
    if file and allowed_file(file.filename, ['text', 'document', 'image', 'audio']):
        filename = secure_filename(file.filename)
        temp_path = os.path.join(tempfile.gettempdir(),filename)
        file.save(temp_path)
        
        file_ext = filename.rsplit('.', 1)[1].lower()
        text = ""
        
        # Process based on file type
        if file_ext in ALLOWED_EXTENSIONS['text']:
            with open(temp_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif file_ext == 'pdf':
            text = ocr_processor.process_pdf(temp_path)
        elif file_ext in ALLOWED_EXTENSIONS['image']:
            text = ocr_processor.process_image(temp_path)
            # If text is too short, try handwriting detection
            if len(text.strip()) < 50:
                text = ocr_processor.detect_handwriting(temp_path)
        elif file_ext in ALLOWED_EXTENSIONS['audio']:
            text = speech_processor.process_audio(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        # Check if text extraction was successful
        if not text or len(text.strip()) == 0:
            return jsonify({'error': 'Could not extract text from the file'}), 400
            
        # Get parameters for summarization
        length = request.form.get('length', 'medium')  # short, medium, large
        output_format = request.form.get('format', 'paragraph')  # paragraph, bullets, mindmap
        
        # Generate summary or mindmap
        if output_format == 'mindmap':
            result = mindmap_generator.generate_mindmap(text)
        else:
            result = summarizer.summarize(text, length, output_format)
        
        return jsonify({
            'original_text': text,
            'summary': result
        })
    
    return jsonify({'error': 'File type not allowed'}), 400