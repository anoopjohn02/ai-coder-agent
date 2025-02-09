from typing import Any, Dict

from langchain.prompts import (ChatPromptTemplate,
                               HumanMessagePromptTemplate, MessagesPlaceholder)
from langchain.schema import SystemMessage
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

from app.config import CUSTOM_PROMPT
from app.services.conversation import get_messages_by_conversation_id
from ..state import GraphState
from ...llms import build_coder_llm

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=CUSTOM_PROMPT),
        MessagesPlaceholder(variable_name="context"),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)


async def generate_output_node(state: GraphState) -> Dict[str, Any]:
    question = state.get("refined_question", state["question"])
    conversation_id = state["conversation_id"]
    conversations = get_messages_by_conversation_id(conversation_id)

    llm = build_coder_llm(state, True)
    chain = prompt | llm | StrOutputParser()
    answer = await chain.ainvoke({"question": question, "chat_history": [conversations]})

    messages = [HumanMessage(content=state["question"]), AIMessage(content=answer)]
    return {"answer": answer, "messages": messages}
