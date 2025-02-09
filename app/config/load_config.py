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
    static_path = os.getenv('STATIC_FILE_PATH')


class Db:
    """
    Store DB related configurations
    """
    schema = os.getenv('DB_SCHEMA')
    connUrl = os.getenv('DB_CONNECTION_URL')


class OllamaConfig:
    """
    Store OpenAI specific configurations
    """
    DEFAULT_MODEL_NAME = os.getenv('DEFAULT_MODEL_NAME')
    CODER_MODEL_NAME = os.getenv('CODER_MODEL_NAME')
