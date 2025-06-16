import glob
import os
from modules.file_reader import read_pdf_files, read_word_files
from modules.file_writer import fill_template
from modules.ollama_integration import ollama_query
from modules.template_selector import list_templates


def main():
    print("Welcome to the Engineering Documentation Assistant!")
    print("Please select a task:")
    print("1. Language Translation")
    print("2. Grammar Check")
    print("3. Document Auto-Completion")

    # Prompt user to choose a task
    choice = input("Enter your choice (1/2/3): ")

    # Prompt the user for file type and folder path
    file_type = input("Are your input files PDF or Word documents? (Enter 'pdf' or 'docx'): ").lower()
    folder_path = input("Enter the folder path containing the input files: ")

    if file_type == "pdf":
        # Collect all PDFs in the folder and read their text
        input_files = glob.glob(f"{folder_path}/*.pdf")
        if not input_files:
            print("No PDF files found in the folder.")
            return
        combined_text = read_pdf_files(input_files)
    elif file_type == "docx":
        # Collect all Word files in the folder and read their text
        input_files = glob.glob(f"{folder_path}/*.docx")
        if not input_files:
            print("No Word files found in the folder.")
            return
        combined_text = read_word_files(input_files)
    else:
        print("Unsupported file type.")
        return

    # Action based on user selection
    if choice == "1":  # Language Translation
        language = input("Enter target language for translation (e.g., en, es, fr): ")
        prompt = f"Translate this text to {language}:\n{combined_text}"
        result = ollama_query(prompt)
        print("Translation Result:\n", result)
    elif choice == "2":  # Grammar Check
        prompt = f"Check and correct grammar for this text:\n{combined_text}"
        result = ollama_query(prompt)
        print("Grammar Check Result:\n", result)
    elif choice == "3":  # Document Auto-Completion
        template_folder = "templates"
        templates = list_templates(template_folder)  # Dynamically list templates
        template_choice = int(input("Select a template by number: "))
        template_path = os.path.join(template_folder, templates[template_choice - 1])  # Get template path

        output_path = input("Enter the path to save your completed document (e.g., output.docx): ")
        
        # Collect placeholders and values
        placeholders = {}
        print("Enter placeholders and values (type 'done' to finish):")
        while True:
            placeholder = input("Placeholder (e.g., {NAME}): ")
            if placeholder.lower() == 'done':
                break
            value = input("Value: ")
            placeholders[placeholder] = value

        # Fill placeholders in the selected template
        fill_template(template_path, output_path, placeholders)
        print(f"Document has been saved to {output_path}.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()