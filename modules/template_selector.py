import os

def list_templates(template_folder):
    """Lists all Word templates dynamically in the 'templates' folder."""
    templates = [f for f in os.listdir(template_folder) if f.endswith('.docx')]
    print("Available Templates:")
    for idx, template in enumerate(templates, start=1):
        print(f"{idx}. {template}")
    return templates