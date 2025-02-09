"""
Repository module
"""

from sqlalchemy import select

from .entities import (ConversationHistory,
                       ConversationMessage)
from .sql_engine import Session


class ConversationRepo:
    """
    Conversation Repo
    """

    def save_conversation(self, conversation: ConversationHistory):
        """
        Method to save conversations
        """
        with Session() as session:
            session.add(conversation)
            session.commit()

    def get_conversation(self, conv_id):
        """
        Method to fetch one conversations
        """
        with Session() as session:
            stmt = select(ConversationHistory).where(ConversationHistory.id == conv_id)
            return session.scalars(stmt).one()

    def get_user_conversations(self, user_id):
        """
        Method to fetch user conversations
        """
        with Session() as session:
            stmt = select(ConversationHistory).where(ConversationHistory.user_id == user_id,
                                                     ConversationHistory.deleted == False)
            return session.scalars(stmt).all()


class ConversationMessageRepo:
    """
    Conversation Message Repo
    """

    def save_message(self, message: ConversationMessage):
        """
        Method to save a message
        """
        with Session() as session:
            session.add(message)
            session.commit()

    def get_conversation_messages(self, conv_id):
        """
        Method to fetch messages related to given conversation
        """
        with Session() as session:
            stmt = select(ConversationMessage).where(ConversationMessage.conversation_id == conv_id)
            return session.scalars(stmt).all()

    def get_txn_messages(self, txn_id):
        """
        Method to fetch messages related to given conversation
        """
        with Session() as session:
            stmt = select(ConversationMessage).where(ConversationMessage.transaction_id == txn_id)
            return session.scalars(stmt).all()

    def get_n_conversation_messages(self, n, conv_id):
        """
        Method to fetch last N messages related to given conversation
        """
        with Session() as session:
            stmt = select(ConversationMessage).where(ConversationMessage.conversation_id == conv_id).order_by(
                ConversationMessage.created_on.desc()).limit(n)
            return session.scalars(stmt).all()
