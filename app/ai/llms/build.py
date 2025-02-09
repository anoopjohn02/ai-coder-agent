"""
LLM Build Module
"""

from app.config import OllamaConfig as config
from .ollama import build_ollama_llm
from ..graph.state import GraphState


def build_coder_llm(state: GraphState, streaming: bool):
    """
    Build LLM Function
    """
    handlers = []
    return build_ollama_llm(config.CODER_MODEL_NAME, streaming, handlers)


def default_llm(state: GraphState, streaming: bool):
    """
    Build LLM for Router
    """
    handlers = []
    return build_ollama_llm(config.DEFAULT_MODEL_NAME, streaming, handlers)
