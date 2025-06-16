import requests


def ollama_query(prompt, model='latest'):
    """
    Sends a query to the Ollama model API and retrieves the response.
    :param prompt: Text or query for the model.
    :param model: Model name (e.g., 'latest').
    :return: Response from the model.
    """
    url = f"http://localhost:8000/api/{model}"  # Adjust this if the API URL changes
    payload = {'prompt': prompt}
    response = requests.post(url, json=payload)  # Make POST request with JSON payload

    if response.status_code == 200:  # Check for success
        return response.json().get('response')  # Return model output
    else:
        raise Exception(f"Ollama API Error: {response.text}")  # Raise an error for failed requests