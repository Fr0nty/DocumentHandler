# DocumentHandler
## Installing Ollama
Firstly you need to install Ollama on your local machine form this site: https://ollama.com/ <br>
This will serve as the interpreter of the documents. Once it has finished installing run the command it shows in the cmd to install the first llm (llama3.2). For more details about using Ollama you can check out their official readme here: https://github.com/ollama/ollama/blob/main/README.md <br>
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

## Setting up for usage
After you have installed the program you girst need to update the data folder and the template folder. <br>
The data folder will see your inputs, meaning the files that need to be processed, while the template folder will act as the place for setting up how you want that data to be processed.

## Issues and how to overcome
After adressing the previous issues, the code works both on translation and grammar fixing, now the real challenge is to make it rewrite it into the specific template format, there might be need for additional processing by a multi modal model like llava to realize the paper layout with both the figures and tables, as well as the text positioning, remains to be tested and seen what solution might work.

## Other branches
I made another branch that I will treat a little different, instead of writing the text directly in the word after the llm process it, I will process it in a Json and try to split it into 4 main components: header, main text, table, figure.<br>
After this split is done, I will try and use the python that handles word documents in order to make a more correct template setup. It may not be possible to copy paste figures and images from the text, that would be the only issue, but I am sure I can find another solution for this problem.