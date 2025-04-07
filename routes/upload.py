from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import uuid
import tempfile

upload_routes = Blueprint('upload_routes', __name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'text': {'txt', 'md', 'rtf'},
    'document': {'pdf', 'docx'},
    'image': {'png', 'jpg', 'jpeg', 'gif', 'bmp'},
    'audio': {'mp3', 'wav', 'ogg', 'm4a'}
}

def allowed_file(filename, file_types):
    """Check if file extension is allowed."""
    extensions = set()
    for file_type in file_types:
        extensions.update(ALLOWED_EXTENSIONS.get(file_type, set()))
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@upload_routes.route('/', methods=['POST'])
def upload_file():
    """General file upload endpoint."""
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    # Process file if allowed
    if file and allowed_file(file.filename, ['text', 'document', 'image', 'audio']):
        # Generate unique filename to prevent collisions
        original_filename = secure_filename(file.filename)
        file_ext = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        
        # Save file
        temp_path = os.path.join(tempfile.gettempdir(), unique_filename)
        file.save(temp_path)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': unique_filename,
            'originalFilename': original_filename,
            'path': temp_path
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@upload_routes.route('/types', methods=['GET'])
def get_allowed_types():
    """Return the allowed file types."""
    return jsonify(ALLOWED_EXTENSIONS)