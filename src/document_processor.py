
import PyPDF2
from docx import Document
from pathlib import Path

class DocumentProcessor:
    
    def extract_text(self, file_path):
        """
        Automatically detect PDF or DOCX and extract text.
        """
        file_ext = Path(file_path).suffix.lower()

        if file_ext == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif file_ext == ".docx":
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        return text
    
    def extract_text_from_docx(self, docx_path):
        """Extract text from Word document"""
        doc = Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text
    
    def chunk_text(self, text, chunk_size=2000):
        """Split text into manageable chunks"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunks.append(" ".join(words[i:i + chunk_size]))
        return chunks
