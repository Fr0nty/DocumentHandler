# DocumentHandler

Firstly you need to install Ollama on your local machine form this site: https://ollama.com/ \n
This will serve as the interpreter of the documents. Once it has finished installing run the command it shows in the cmd to install the first llm (llama3.2). For more details about using Ollama you can check out their official readme here: https://github.com/ollama/ollama/blob/main/README.md \n
You can install more powerful models but make sure you have enough space available:

| Model                | Parameters | Size   | Download                         |
|----------------------|------------|--------|----------------------------------|
| Gemma 3             | 1B         | 815MB  | `ollama run gemma3:1b`           |
| Gemma 3             | 4B         | 3.3GB  | `ollama run gemma3`              |
| Gemma 3             | 12B        | 8.1GB  | `ollama run gemma3:12b`          |
| Gemma 3             | 27B        | 17GB   | `ollama run gemma3:27b`          |
| QwQ                 | 32B        | 20GB   | `ollama run qwq`                 |
| DeepSeek-R1         | 7B         | 4.7GB  | `ollama run deepseek-r1`         |
| DeepSeek-R1         | 671B       | 404GB  | `ollama run deepseek-r1:671b`    |
| Llama 4             | 109B       | 67GB   | `ollama run llama4:scout`        |
| Llama 4             | 400B       | 245GB  | `ollama run llama4:maverick`     |
| Llama 3.3           | 70B        | 43GB   | `ollama run llama3.3`            |
| Llama 3.2           | 3B         | 2.0GB  | `ollama run llama3.2`            |
| Llama 3.2           | 1B         | 1.3GB  | `ollama run llama3.2:1b`         |
| Llama 3.2 Vision    | 11B        | 7.9GB  | `ollama run llama3.2-vision`     |
| Llama 3.2 Vision    | 90B        | 55GB   | `ollama run llama3.2-vision:90b` |
| Llama 3.1           | 8B         | 4.7GB  | `ollama run llama3.1`            |
| Llama 3.1           | 405B       | 231GB  | `ollama run llama3.1:405b`       |
| Phi 4               | 14B        | 9.1GB  | `ollama run phi4`                |
| Phi 4 Mini          | 3.8B       | 2.5GB  | `ollama run phi4-mini`           |
| Mistral             | 7B         | 4.1GB  | `ollama run mistral`             |
| Moondream 2         | 1.4B       | 829MB  | `ollama run moondream`           |
| Neural Chat         | 7B         | 4.1GB  | `ollama run neural-chat`         |
| Starling            | 7B         | 4.1GB  | `ollama run starling-lm`         |
| Code Llama          | 7B         | 3.8GB  | `ollama run codellama`           |
| Llama 2 Uncensored  | 7B         | 3.8GB  | `ollama run llama2-uncensored`   |
| LLaVA               | 7B         | 4.5GB  | `ollama run llava`               |
| Granite-3.3         | 8B         | 4.9GB  | `ollama run granite3.3`          |