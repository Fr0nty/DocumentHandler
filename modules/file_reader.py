from PyPDF2 import PdfReader
from docx import Document


def read_pdf_files(file_paths):
    """
    Reads and combines text from multiple PDF files.
    :param file_paths: List of paths to PDF files.
    :return: Combined text from all PDFs.
    """
    combined_text = ""
    for file_path in file_paths:
        reader = PdfReader(file_path)
        for page in reader.pages:
            combined_text += page.extract_text() + "\n"  # Combine extracted text
    return combined_text


def read_word_files(file_paths):
    """
    Reads and combines text from multiple Word files.
    :param file_paths: List of paths to Word (.docx) files.
    :return: Combined text from all Word files.
    """
    combined_text = ""
    for file_path in file_paths:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            combined_text += paragraph.text + "\n"  # Combine paragraph text
    return combined_text