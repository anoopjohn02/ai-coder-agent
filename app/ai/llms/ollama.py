from langchain_core.callbacks import BaseCallbackHandler
from langchain_ollama import ChatOllama


def build_ollama_llm(model: str, streaming: bool,
                     handlers: [BaseCallbackHandler]):
    """
    Build Ollama Model
    Args:
        model(str): Ollama model name
        streaming(bool): Enable streaming
        handlers(BaseCallbackHandler): Callback Handlers
    """
    return ChatOllama(
        streaming=streaming,
        model=model,
        callbacks=handlers,
    )
