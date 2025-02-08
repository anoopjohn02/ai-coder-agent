"""
load config module
"""
import os

from dotenv import load_dotenv

load_dotenv()

PDF_DIRECTORY = 'docs'
METADATA_FILE = 'document_metadata.json'

class App:
    """
    Store app specific configurations
    """
    PORT = 8080

class Db:
    """
    Store DB related configurations
    """
    schema = os.getenv('DB_SCHEMA')
    connUrl = os.getenv('DB_CONNECTION_URL')

class OpenaiConfig:
    """
    Store OpenAI specific configurations
    """
    MODEL_NAME = os.getenv('OPEN_AI_MODEL')
    EMBEDDING_MODEL = "text-embedding-ada-002"

class OllamaConfig:
    """
    Store OpenAI specific configurations
    """
    MODEL_NAME = os.getenv('OLLAMA_MODEL')

class DeepSeekConfig:
    """
    Store Deepseek specific configurations
    """
    MODEL_NAME = os.getenv('DEEP_SEEK_MODEL')

