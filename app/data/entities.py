"""
Entity module
"""
import uuid
from datetime import datetime
from typing import List

from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
from sqlalchemy import DateTime, MetaData, Column
from sqlalchemy import ForeignKey
from sqlalchemy import String, Boolean, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
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

class ConversationSummary(Base):
    """
    Conversation Summary Class
    """
    __tablename__ = "conversation_summary"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("conversation_history.id"))
    summary: Mapped[str]
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow)

class MessageTokenUsage(Base):
    """
    Conversation Message Class
    """
    __tablename__ = "messages_token_usage"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    conversation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("conversation_history.id"))
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    prompt_tokens: Mapped[int] = mapped_column(Integer)
    output_tokens: Mapped[int] = mapped_column(Integer)
    prompt_cost: Mapped[int] = mapped_column(Numeric)
    output_cost: Mapped[int] = mapped_column(Numeric)
    embedding_cost: Mapped[int] = mapped_column(Numeric)
    llm_model: Mapped[str] = mapped_column(String(30))
    embedding_model: Mapped[str] = mapped_column(String(30))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    created_on = Column(DateTime, default=datetime.utcnow)
    conversation_history: Mapped["ConversationHistory"] = relationship(
        "ConversationHistory", lazy='joined'
    )

class DocumentEmbedding(Base):
    """
    Document Embedding Class
    """
    __tablename__ = "document_embedding"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    embedding_model: Mapped[str] = mapped_column(String(30))
    chunk_size: Mapped[int] = mapped_column(Integer)
    chunk_overlap: Mapped[int] = mapped_column(Integer)
    token_encoding_model: Mapped[str] = mapped_column(String(30))
    files: Mapped[List["DocumentEmbeddingFiles"]] = relationship(
         back_populates="embedding", cascade="all, delete-orphan", lazy="subquery"
     )

class DocumentEmbeddingFiles(Base):
    """
    Document Embedding File Class
    """
    __tablename__ = "document_embedding_files"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    embedding_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document_embedding.id"))
    file_name: Mapped[str] = mapped_column(String(30))
    num_chunks: Mapped[int] = mapped_column(Integer)
    num_tokens: Mapped[int] = mapped_column(Integer)
    processed_date: Mapped[datetime] = mapped_column(DateTime)
    last_modified: Mapped[datetime] = mapped_column(DateTime)
    embedding: Mapped["DocumentEmbedding"] = relationship(back_populates="files")

class Devices(Base):
    """
    Devices Class
    """
    __tablename__ = "devices"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(30))
    created_on = Column(DateTime, default=datetime.utcnow)
    user_id: Mapped[uuid.UUID]