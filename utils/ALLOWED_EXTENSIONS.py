# This goes at the top of summarizer_api.py
ALLOWED_EXTENSIONS = {
    'text': {'txt', 'md'},
    'document': {'pdf', 'docx'},
    'image': {'jpg', 'jpeg', 'png'},
    'audio': {'mp3', 'wav'}
}


def allowed_file(filename, file_types):
    if '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()
    extensions = set()

    for file_type in file_types:
        extensions.update(ALLOWED_EXTENSIONS.get(file_type, set()))

    return ext in extensions
