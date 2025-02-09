"""
Conversation module
"""
import uuid

from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage

from app.data.entities import ConversationHistory, ConversationMessage
from app.data.repo import ConversationMessageRepo, ConversationRepo
from .exceptions import ServiceException

conversationRepo = ConversationRepo()
messageRepo = ConversationMessageRepo()


def get_messages_by_conversation_id(
        conversation_id: uuid,
) -> [AIMessage | HumanMessage | SystemMessage]:
    """
    Finds all messages that belong to the given conversation_id

    :param conversation_id: The id of the conversation

    :return: A list of messages
    """
    messages = messageRepo.get_conversation_messages(conversation_id)
    return [message.as_lc_message() for message in messages]


def get_messages_by_transaction_id(
        txn_id: uuid,
) -> [AIMessage | HumanMessage | SystemMessage]:
    """
    Finds all messages that belong to the given transaction_id

    :param txn_id: The id of the transaction

    :return: A list of messages
    """
    messages = messageRepo.get_txn_messages(txn_id)
    return [message.as_lc_message() for message in messages]


def get_last_messages_by_count(
        conversation_id: uuid, n: int
) -> [AIMessage | HumanMessage | SystemMessage]:
    """
    Finds last n messages that belong to the given conversation_id

    :param conversation_id: The id of the conversation
    :param n: number of messages

    :return: A list of messages
    """
    messages = messageRepo.get_n_conversation_messages(n, conversation_id)
    return [message.as_lc_message() for message in messages]


def add_message_to_conversation(
        conversation_id: uuid, role: str, content: str, transaction_id: uuid
):
    """
    Creates aa new message tied to the given conversation_id
        with the provided role and content

    :param conversation_id: The id of the conversation
    :param role: The role of the message
    :param content: The content of the message
    :param transaction_id: The id of the transaction

    :return: void
    """
    message = ConversationMessage()
    message.id = uuid.uuid1()
    message.transaction_id = transaction_id
    message.conversation_id = conversation_id
    message.role = role
    message.content = content
    messageRepo.save_message(message)


def create_new_user_conversation(user_id: uuid) -> uuid:
    """
    Function will provide new conversation for the user and return conversation id.
    If conversation doesn't exist it will create one.

    :param user_id: The id of the user

    :return: The conversation id
    """
    conversations = conversationRepo.get_user_conversations(user_id)
    for conversation in conversations:
        conversation.deleted = True
        conversationRepo.save_conversation(conversation)
    id = uuid.uuid1()
    create_conv = ConversationHistory()
    create_conv.id = id
    create_conv.user_id = user_id
    create_conv.retriever = ""
    create_conv.memory = ""
    create_conv.llm = ""
    create_conv.deleted = False
    conversationRepo.save_conversation(create_conv)
    return id


def get_default_user_conversation(user_id: uuid) -> uuid:
    """
    Function will provide existing conversation id for the user.
    If conversation doesn't exist it will create one.

    :param user_id: The id of the user

    :return: The conversation id
    """
    conversations = conversationRepo.get_user_conversations(user_id)
    if len(conversations) > 0:
        return conversations[0].id
    else:
        raise ServiceException(f"Unable to find any previous conversation for user {user_id}")
