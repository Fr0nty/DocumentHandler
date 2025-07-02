import os
import PyPDF2
import json
import requests  # For interacting with the Ollama server

# Ollama config
endpoint = "http://localhost:11434/api/generate"  # Replace with your local Ollama server URL
MODEL_NAME = "mistral"
MAX_TOKENS = 6000
CHARACTER_LIMIT = 24000  # Roughly for ~6000 tokens

def extract_pdf_text(file_path):
    """Extracts text from the given PDF file."""
    text = ""
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def transform_text_via_ollama(input_text, translate_to=None):
    """
    Perform transformation using Ollama (local model).
    - input_text: content from the old PDF
    - translate_to: optional target language (e.g., Romanian)
    """
    prompt = f"""
    Correct the grammar and improve the clarity of the following text.
    If needed, translate this content into {translate_to}:
    Write only the final version after you make all the changes, if the content is translated in {translate_to}, write only the translation.
    ---
    Content:
    {input_text}
    ---
    """
    
    # Making a POST request to the local Ollama server
    payload = {
        "model": MODEL_NAME,  # Specify the model name
        "prompt": prompt
    }
    try:
        response = requests.post(endpoint, json=payload)
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
                except json.JSONDecodeError:
                    pass

        # Return the full assembled response
        return full_response_data.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error during Ollama processing: {e}")
        return None

def save_to_json(data, output_path):
    """Saves the data to a JSON file."""
    with open(output_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main():
    # Folders
    data_folder = "data"
    output_folder = "output"
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

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
    
    # Step 2: Transformation Type
    transform_choice = input("\nDo you want to translate the document? (y/n): ").strip().lower()
    translate_to = None
    if transform_choice == "y":
        translate_to = input("Enter the target language (e.g., Romanian): ").strip()
    
    # Process
    print("\nProcessing...")
    pdf_text = extract_pdf_text(pdf_path)

    # Categorize the text
    categorized_data = {
        "header": [],
        "main text": [],
        "figure": [],
        "table": []
    }

    # Simple heuristic to categorize the text
    paragraphs = pdf_text.strip().split("\n")
    current_category = "main text"  # Default

    for paragraph in paragraphs:
        if paragraph.strip().startswith("Pagina"):
            current_category = "header"
        elif "Tabelul" in paragraph or "Cerinte" in paragraph:
            current_category = "table"
        elif any(figure_keyword in paragraph for figure_keyword in ["Figura", "Photo", "Figure", "Baldovineti"]):
            current_category = "figure"

        # Transform the text
        transformed_paragraph = transform_text_via_ollama(paragraph, translate_to)
        if transformed_paragraph:
            categorized_data[current_category].append(transformed_paragraph)

    # Save output to JSON
    output_file = f"{os.path.splitext(pdf_files[pdf_choice])[0]}_formatted.json"
    output_path = os.path.join(output_folder, output_file)
    save_to_json(categorized_data, output_path)
    
    print(f"\nDocument has been reformatted and saved to {output_path}")

if __name__ == "__main__":
    main()