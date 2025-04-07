from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Configure CORS to allow requests from your frontend
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Configure uploads
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
    
    # Register blueprints
    from routes.summarizer_api import summarizer_api
    from routes.ocr_api import ocr_api
    from routes.stt_api import stt_api
    from routes.upload import upload_routes
    
    app.register_blueprint(summarizer_api, url_prefix='/api/summarizer')
    app.register_blueprint(ocr_api, url_prefix='/api/ocr')
    app.register_blueprint(stt_api, url_prefix='/api/stt')
    app.register_blueprint(upload_routes, url_prefix='/api/upload')
    
    @app.route('/')
    def home():
        return {
            "status": "online",
            "message": "AI Notes Summarizer API is running"
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)