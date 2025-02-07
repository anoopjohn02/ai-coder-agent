"""
Auth Module
"""
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TokenUser(BaseModel):
    """
    Token User Dto
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class User(BaseModel):
    """
    User Dto
    """
    id: UUID
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class LoggedInUser(BaseModel):
    """
    Logged In User class
    """
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    realm_roles: list
    client_roles: list
