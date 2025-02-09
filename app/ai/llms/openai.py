"""
OpenAI Module
"""
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.config import OpenaiConfig as config

def build_openai_llm(streaming: bool,
                     handlers: [BaseCallbackHandler]):
    """
    Build OpenAI Model
    Args:
        streaming(bool): Enable streaming
        handlers(BaseCallbackHandler): Callback Handlers
    """
    return ChatOpenAI(
        streaming=streaming,
        model_name=config.MODEL_NAME,
        callbacks=handlers,
    )

