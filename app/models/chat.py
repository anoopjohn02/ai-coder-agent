"""
Chat Module contains chat models
"""

from pydantic import BaseModel


class Request(BaseModel):
    """
    Chat request from client
    """
    question: str
    new_chat: bool

class Response(BaseModel):
    """
    Chat response
    """
    text: str

