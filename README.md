# AI Coder Agent #

This is an AI-driven chatbot that generate and review code. 

Once you have run the application go to [http://localhost:8080/ui](http://localhost:8080/ui) to see the chatbot

### Libraries used: ###

* Python
* LangChain/LangGraph - Framework
* OpenAI/LLAMA - LLM
* DeepSeek-Coder - Code generator/review Model
* FastApi - APIs
* SQLAlchemy - ORM
* jinja - UI / Template


### Set ENV variable ###

* Clone the repository
* Create .env file at root and add the following

| name               | possible values                                                    | 
|--------------------|--------------------------------------------------------------------|
| DB_CONNECTION_URL  | postgresql+psycopg2://postgres:postgres@localhost:5432/coder_agent | 
| DB_SCHEMA          | ai_coder_agent                                                     |
| OPENAI_API_KEY     |                                                                    |
| OPEN_AI_MODEL      | gpt-4o, gpt-4o-mini                                                | 
| CODER_MODEL_NAME   | deepseek-coder-v2                                                  |
| DEFAULT_MODEL_NAME | llama3.2                                                           |
| STATIC_FILE_PATH   | path/to/root/folder                                                |

## How do I set up locally? ##

### Prerequisite ###

Following should be installed in machine

* Python 3.11
* Docker if required

Run following command to make sure python installed and configured

    python --version

## Ollama ##

Install Ollama latest version from https://ollama.com/.
Then, Pull llama3.2

    ollama pull llama3.2

Pull deepseek-coder

    ollama pull deepseek-coder-v2

### Run application ###
Install [PIP](https://pip.pypa.io/en/stable/installation/)

Run
    
    pip install pipenv

Run command to install dependencies

    pipenv install

Run command to load ENV variables to virtual env

    pipenv shell
