from typing import Any, Dict

from langchain.prompts import (ChatPromptTemplate,
                               HumanMessagePromptTemplate, MessagesPlaceholder)
from langchain.schema import SystemMessage
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

from app.services.conversation import get_messages_by_conversation_id
from ..state import GraphState
from ...llms import build_coder_llm

REVIEW_PROMPT = """
You are an expert software reviewer with deep knowledge of programming best practices, performance optimization, security, scalability, and maintainability. The user will provide a piece of code, and your task is to review it thoroughly.

Provide structured feedback covering the following aspects:

1. Code Quality: Assess readability, maintainability, and adherence to best practices.
2. Performance: Identify potential bottlenecks and suggest optimizations.
3. Security: Highlight any security vulnerabilities and recommend improvements.
4. Scalability: Comment on whether the code can handle increasing workloads efficiently.
5. Correctness: Ensure the code functions as intended and follows logical correctness.
6. Best Practices: Suggest improvements based on industry standards and conventions.
7. Documentation & Naming: Evaluate clarity in variable names, function names, and inline documentation.

Provide actionable suggestions for improvement along with code snippets where necessary. Be clear, concise, and constructive in your feedback. 

"""

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=REVIEW_PROMPT),
        MessagesPlaceholder(variable_name="context"),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)


async def review_output_node(state: GraphState) -> Dict[str, Any]:
    question = state.get("refined_question", state["question"])
    conversation_id = state["conversation_id"]
    conversations = get_messages_by_conversation_id(conversation_id)

    llm = build_coder_llm(state, True)
    chain = prompt | llm | StrOutputParser()
    answer = await chain.ainvoke({"question": question, "chat_history": [conversations]})

    messages = [HumanMessage(content=state["question"]), AIMessage(content=answer)]
    return {"answer": answer, "messages": messages}
