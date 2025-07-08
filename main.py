import os
import pdfplumber
import json
import requests  # For interacting with the Ollama server

# Ollama config
endpoint = "http://localhost:11434/api/generate"  # Replace with your local Ollama server URL
MODEL_NAME = "mistral"
CHARACTER_LIMIT = 24000  # Roughly for ~6000 tokens
BATCH_SIZE = 5  # Number of paragraphs to process in each batch

def extract_pdf_text(file_path):
    """Extracts text from the given PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def transform_text_via_ollama(batch_text, translate_to=None):
    """
    Perform transformation using Ollama (local model) in batches.
    - batch_text: combined content from the PDF
    - translate_to: optional target language (e.g., Romanian)
    """
    prompt = f"""
    Correct the grammar and improve the clarity of the following text, don't try to summarize the text, keep every part of it, reformulate only when absolutely necessary.
    Detect in what language this content was written and don't try to change this.
    Write only the final version after you make all the changes, if the content is translated in {translate_to}, write only the translation.
    ---
    Content:
    {batch_text}
    ---
    """
    
    # Making a POST request to the local Ollama server
    payload = {
        "model": MODEL_NAME,
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
    print(f"Extracted text from {pdf_files[pdf_choice]}:\n{pdf_text[:500]}...\n")  # Display first 500 chars

    # Categorize the text
    categorized_data = {
        "main text": [],
        "table": []
    }

    # Split text into paragraphs
    paragraphs = pdf_text.strip().split("\n")
    batch = []

    # Process paragraphs in batches
    for paragraph in paragraphs:
        if "Tabelul" in paragraph or "Cerinte" in paragraph:
            categorized_data["table"].append(paragraph)  # Add directly to tables
            print(f"Categorizing as table: {paragraph}")
        else:
            batch.append(paragraph)  # Add to batch for main text
        
        # Process the batch when it reaches the specified size
        if len(batch) >= BATCH_SIZE:
            batch_text = "\n".join(batch)  # Join the paragraphs into a single batch
            print(f"Transforming main text batch:\n{batch_text[:100]}...\n")  # Preview first 100 chars of the batch
            transformed_batch = transform_text_via_ollama(batch_text, translate_to)
            if transformed_batch:
                categorized_data["main text"].append(transformed_batch)
            batch = []  # Reset the batch

    # Process any remaining paragraphs in the last batch
    if batch:
        batch_text = "\n".join(batch)
        print(f"Transforming final main text batch:\n{batch_text[:100]}...\n")  # Preview first 100 chars of the last batch
        transformed_batch = transform_text_via_ollama(batch_text, translate_to)
        if transformed_batch:
            categorized_data["main text"].append(transformed_batch)

    # Save output to JSON
    output_file = f"{os.path.splitext(pdf_files[pdf_choice])[0]}_formatted.json"
    output_path = os.path.join(output_folder, output_file)
    save_to_json(categorized_data, output_path)
    
    print(f"\nDocument has been reformatted and saved to {output_path}")

if __name__ == "__main__":
    main()