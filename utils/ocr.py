try:
    import pytesseract
    from PIL import Image
    import fitz  # PyMuPDF
    import cv2
    import numpy as np
    import os
except ImportError:
    pytesseract = None
    Image = None
    fitz = None


def preprocess_image(image_path):
    """Preprocess image for better OCR accuracy."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
    return processed


def process_image(image_path, lang='eng'):
    """Extract text from an image using OCR."""
    if not pytesseract or not Image:
        return "OCR libraries not installed."

    try:
        processed = preprocess_image(image_path)
        text = pytesseract.image_to_string(processed, lang=lang)
        return text
    except Exception as e:
        return f"Error processing image: {str(e)}"


def detect_handwriting(image_path):
    """Detect handwriting in an image (currently same as process_image)."""
    return process_image(image_path)


def process_pdf(pdf_path, lang='eng'):
    """Extract text from a PDF using PyMuPDF and OCR fallback."""
    if not fitz:
        return "PyMuPDF not installed."

    try:
        doc = fitz.open(pdf_path)
        text = ""

        # Try extracting regular text
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()

        # Fallback to OCR if text is too little
        if len(text.strip()) < 50:
            text = ""
            for page_num in range(len(doc)):
                pix = doc[page_num].get_pixmap()
                img_path = f"temp_page_{page_num}.png"
                pix.save(img_path)
                text += process_image(img_path, lang=lang)
                os.remove(img_path)

        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
