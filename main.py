import os
import PyPDF2
from docx import Document
import requests  # For interacting with the Ollama server
import json

# Ollama config
endpoint = "http://localhost:11434/api/generate"  # Replace with your local Ollama server URL
MODEL_NAME = "llama3.2"


def extract_pdf_text(file_path):
    """Extracts text from the given PDF file."""
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def load_template(template_path):
    """Loads the text/template from the Word document."""
    doc = Document(template_path)
    template_text = ""
    for paragraph in doc.paragraphs:
        template_text += paragraph.text + "\n"
    return template_text


def transform_text_via_ollama(input_text, template_text, translate_to=None):
    """
    Perform transformation using Ollama (local model).
    - input_text: content from the old PDF
    - template_text: structure/format from the Word document
    - translate_to: optional target language (e.g., Romanian)
    """
    prompt = f"""
    Rewrite the following content to match the format below, without changing the information from the content.
    Maintain as much of the original context as possible.
    ---
    Content:
    {input_text}
    ---
    Format:
    {template_text}
    ---
    {"Translate this content into " + translate_to + " if needed or correct the grammar." if translate_to else "Correct the grammar if needed."}
    """

    # Making a POST request to the local Ollama server
    payload = {
        "model": MODEL_NAME,  # Specify the model name
        "prompt": prompt
    }
    print(f"Payload: {payload}")
    try:
        response = requests.post(endpoint, json=payload)
        print(f"Raw response: {response.text}")  # Debugging statement to inspect the response
        response.raise_for_status()  # Raise HTTP errors
        full_response_data = ""
        for chunk in response.iter_lines():
            if chunk:
                try:
                    # Attempt to parse each chunk as JSON
                    chunk_data = json.loads(chunk.decode("utf-8"))
                    full_response_data += chunk_data.get("response", "")
                    if chunk_data.get("done", False):  # Stop if 'done' is true
                        break
                except json.JSONDecodeError as e:
                    print(f"Failed to decode chunk: {e}")

        # Return the full assembled response
        return full_response_data.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error during Ollama processing: {e}")
        return None


def save_to_word(transformed_text, output_path):
    """Saves transformed text to a Word document."""
    doc = Document()
    for line in transformed_text.split("\n"):
        doc.add_paragraph(line)
    doc.save(output_path)


def main():
    # Folders
    data_folder = "data"
    templates_folder = "templates"
    output_folder = "output"
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # User interaction (basic for CLI)
    print("Welcome to the Documentation Formatter App!")
    
    # Step 1: Select PDF file
    pdf_files = [f for f in os.listdir(data_folder) if f.endswith(".pdf")]
    if not pdf_files:
        print("No PDF files found in the data directory.")
        return
    
    print("Available PDF files:")
    for idx, file in enumerate(pdf_files):
        print(f"{idx + 1}. {file}")
    
    pdf_choice = int(input("Choose a PDF file by number: ")) - 1
    pdf_path = os.path.join(data_folder, pdf_files[pdf_choice])
    
    # Step 2: Select Template
    template_files = [f for f in os.listdir(templates_folder) if f.endswith(".docx")]
    if not template_files:
        print("No template files found in the templates directory.")
        return
    
    print("\nAvailable Templates:")
    for idx, file in enumerate(template_files):
        print(f"{idx + 1}. {file}")
    
    template_choice = int(input("Choose a template by number: ")) - 1
    template_path = os.path.join(templates_folder, template_files[template_choice])
    
    # Step 3: Transformation Type
    transform_choice = input("\nDo you want to translate the document? (y/n): ").strip().lower()
    translate_to = None
    if transform_choice == "y":
        translate_to = input("Enter the target language (e.g., Romanian): ").strip()
    
    # Process
    print("\nProcessing...")
    pdf_text = extract_pdf_text(pdf_path)
    template_text = load_template(template_path)

    # Break the text into larger chunks (for example, each page or 3-5 paragraphs each)
    paragraphs = pdf_text.strip().split("\n")
    chunk_size = 5  # For example, 5 paragraphs per chunk
    chunks = ['\n'.join(paragraphs[i:i + chunk_size]) for i in range(0, len(paragraphs), chunk_size)]

    transformed_texts = []

    for chunk in chunks:
        if chunk.strip():  # Skip empty chunks
            transformed_chunk = transform_text_via_ollama(chunk, template_text, translate_to)
            if transformed_chunk:
                transformed_texts.append(transformed_chunk)

    # Combine the transformed text
    final_transformed_text = "\n".join(transformed_texts)

    # Save output
    output_file = f"{os.path.splitext(pdf_files[pdf_choice])[0]}_formatted.docx"
    output_path = os.path.join(output_folder, output_file)
    save_to_word(final_transformed_text, output_path)
    
    print(f"\nDocument has been reformatted and saved to {output_path}")


if __name__ == "__main__":
    main()