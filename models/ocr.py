from PIL import Image
import pytesseract
import pdf2image
import os
import tempfile
from typing import Optional, Dict, Any

class OCRProcessor:
    def __init__(self):
        # Configure pytesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract_executable'
        pass
        
    def process_image(self, image_path: str) -> str:
        """Extract text from an image using OCR."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error processing image: {e}")
            return ""
    
    def process_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF document."""
        try:
            # Create a temporary directory to store PDF pages as images
            with tempfile.TemporaryDirectory() as temp_dir:
                # Convert PDF to images
                images = pdf2image.convert_from_path(pdf_path)
                
                # Process each page
                text_content = []
                for i, image in enumerate(images):
                    # Save page as temporary image
                    temp_image_path = os.path.join(temp_dir, f'page_{i}.png')
                    image.save(temp_image_path, 'PNG')
                    
                    # Extract text from the page
                    page_text = pytesseract.image_to_string(Image.open(temp_image_path))
                    text_content.append(page_text)
                
                # Combine text from all pages
                return "\n\n".join(text_content)
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return ""
            
    def detect_handwriting(self, image_path: str) -> str:
        """Specialized processing for handwritten text."""
        try:
            image = Image.open(image_path)
            
            # Configure tesseract for handwritten text
            custom_config = r'--oem 1 --psm 6'
            text = pytesseract.image_to_string(image, config=custom_config)
            return text
        except Exception as e:
            print(f"Error processing handwritten text: {e}")
            return ""