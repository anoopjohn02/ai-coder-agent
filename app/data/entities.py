"""
Entity module
"""
import uuid
from datetime import datetime
from typing import List

from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
from sqlalchemy import DateTime, MetaData, Column
from sqlalchemy import ForeignKey
from sqlalchemy import String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Db as dbConfig

Base = declarative_base(metadata=MetaData(schema = dbConfig.schema))

class ConversationHistory(Base):
    """
    Conversation History Class
    """
    __tablename__ = "conversation_history"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    retriever: Mapped[str] = mapped_column(String(30))
    memory: Mapped[str] = mapped_column(String(30))
    llm: Mapped[str] = mapped_column(String(30))
    deleted: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[uuid.UUID]
    created_on = Column(DateTime, default=datetime.utcnow)

class ConversationMessage(Base):
    """
    Conversation Message Class
    """
    __tablename__ = "conversation_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("conversation_history.id"))
    transaction_id: Mapped[uuid.UUID]
    role: Mapped[str] = mapped_column(String(30))
    content: Mapped[str]
    created_on = Column(DateTime, default=datetime.utcnow)

    def as_lc_message(self) -> HumanMessage | AIMessage | SystemMessage:
        """
        Create Message based on the role
        """
        if self.role == "human":
            return HumanMessage(content=self.content)
        elif self.role == "ai":
            return AIMessage(content=self.content)
        elif self.role == "system":
            return SystemMessage(content=self.content)
        else:
            raise Exception(f"Unknown message role: {self.role}")
