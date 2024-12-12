# ai/ai_service.py

import ollama
import base64
from io import BytesIO
from PIL import Image
from PyPDF2 import PdfReader
import docx

def encode_image_to_base64(image_file) -> str:
    """Convert an image file-like object to a base64 encoded string."""
    # Use the in-memory file directly (no need for disk path)
    with BytesIO(image_file.read()) as image_bytes:
        return base64.b64encode(image_bytes.getvalue()).decode('utf-8')

SYSTEM_PROMPT = """Act as an OCR assistant. Analyze the provided image and:
1. Recognize all visible text in the image as accurately as possible.
2. Maintain the original structure and formatting of the text.
3. If any words or phrases are unclear, indicate this with [unclear] in your transcription.
Provide only the transcription without any additional comments."""

class AIService:
    def __init__(self, model_type="ollama", model_name="mistral"):
        self.model_type = model_type
        self.model_name = model_name

    def process_request(self, input_data: str,  input_type: str = "text", input_file=None) -> str:
        """ Process input using the selected AI model. """
        
        if input_type == "text":
            return self._process_with_ollama_text(input_data)
        
        elif input_type == "image" :
            return self._process_with_ollama_image(input_data, input_file)
        
        elif input_type == "pdf":
            return self._process_with_pdf(input_data, input_file)
        
        elif input_type == "word":
            return self._process_with_word(input_data, input_file)

        else:
            raise ValueError(f"Unsupported input type: {input_type}")

    def _process_with_ollama_text(self, input_text: str) -> str:
        """ Process the input text using Ollama's model. """
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": input_text}])
        message_content = response.message.content if response.message else "No response from model"
        return message_content




    def _process_with_ollama_image(self, input_text, image_file) -> str:
        """ Process the image by sending it to Ollama's model (e.g., for image captioning or analysis). """
        try:
            base64_image = encode_image_to_base64(image_file)

            response = ollama.chat(model=self.model_name, messages=[{"role": "user", "images": [base64_image], 'content': input_text}])
            
            # Return the model's response
            message_content = response.message.content if response.message else "No response from model"
            return message_content

        except Exception as e:
            return f"Error processing image: {str(e)}"

    def _process_with_pdf(self, pdf_path: str) -> str:
        """ Process a PDF file by extracting text and sending it to the AI model. """
        text = self._extract_text_from_pdf(pdf_path)
        return self._process_with_ollama_text(text)

    def _process_with_word(self, word_path: str) -> str:
        """ Process a Word document by extracting text and sending it to the AI model. """
        text = self._extract_text_from_word(word_path)
        return self._process_with_ollama_text(text)

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """ Extract text from a PDF file. """
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def _extract_text_from_word(self, word_path: str) -> str:
        """ Extract text from a Word document. """
        doc = docx.Document(word_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text
        return text
