import logging
from typing import Any, Dict

from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate

from app.ai.graph.state import GraphState
from app.ai.llms import default_llm
from app.services.conversation import get_last_messages_by_count

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content="""
                    Given the following chat history and a follow up question, 
                    rephrase the follow up question to be a standalone question.
                    """),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)


def refine_question_node(state: GraphState) -> Dict[str, Any]:
    question = state["question"]
    conversation_id = state["conversation_id"]
    logging.info("Re-factoring question for vector db")
    last_messages = get_last_messages_by_count(conversation_id, 3)
    if len(last_messages) == 0:
        return {"refined_question": question}

    llm = default_llm(state, False)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"question": question, "chat_history": last_messages})
    return {"refined_question": response}
