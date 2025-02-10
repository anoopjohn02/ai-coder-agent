"""
Chat service module
"""
import uuid
import logging

from langchain_core.messages import HumanMessage

from app.models.chat import Request
from app.models.user import LoggedInUser
from .conversation import get_default_user_conversation, create_new_user_conversation
from ..ai.graph.consts import GENERATE, REVIEW
from ..ai.graph.graph import graph


async def aanswer(request: Request, user: LoggedInUser):
    """
    Answer the user query async
    """
    if request.new_chat:
        conversation_id = create_new_user_conversation(user.id)
    else:
        conversation_id = get_default_user_conversation(user.id)
    inputs = {
        "question": request.question,
        "user_id": user.id,
        "conversation_id": conversation_id,
        "transaction_id": uuid.uuid1()
    }
    async for msg, metadata in graph.astream(inputs, stream_mode="messages"):
        logging.info(msg)
        if (msg.content and msg.id.startswith("run-")
                and not isinstance(msg, HumanMessage)
                and (metadata["langgraph_node"] == GENERATE or metadata["langgraph_node"] == REVIEW)):
            yield msg.content.replace('\n', '<br>')
