from typing import Any, Dict

from langchain_core.messages import HumanMessage, AIMessage

from app.ai.graph.state import GraphState
from app.services.conversation import add_message_to_conversation


def save_history_node(state: GraphState) -> Dict[str, Any]:
    print("---HISTORY NODE---")
    conversation_id = state["conversation_id"]
    transaction_id = state["transaction_id"]
    messages = state.get("messages", [])
    if len(messages) == 0:
        messages = [HumanMessage(content=state["question"]), AIMessage(content=state["answer"])]
    for message in messages:
        add_message_to_conversation(
            conversation_id=conversation_id,
            role=message.type,
            content=message.content,
            transaction_id=transaction_id
        )
    return {"messages": messages}
