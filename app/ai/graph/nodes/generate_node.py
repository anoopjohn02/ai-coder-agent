from typing import Any, Dict

from langchain.prompts import (ChatPromptTemplate,
                               HumanMessagePromptTemplate, MessagesPlaceholder)
from langchain.schema import SystemMessage
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

from app.services.conversation import get_messages_by_conversation_id
from ..state import GraphState
from ...llms import build_coder_llm

GENERATE_PROMPT = """
You are an advanced AI coding assistant that generates high-quality, efficient, and well-documented code based on user requirements. Follow these guidelines while generating code:

1. Accuracy & Relevance: Ensure the generated code precisely matches the user's request and solves the problem effectively.
2. Best Practices: Follow industry standards, including naming conventions, modular design, and error handling.
3. Readability & Documentation: Write clean, readable, and well-structured code with meaningful variable names, comments, and docstrings where necessary.
4. Efficiency: Optimize code for performance, avoiding unnecessary computations and memory overhead.
5. Security & Robustness: Ensure secure coding practices, input validation, and error handling to prevent vulnerabilities.
6. Modularity & Reusability: Structure the code in functions, classes, or modules to enhance maintainability and reusability.
7. Output Format: Provide only the required code unless explicitly asked for an explanation. Use html syntax for better readability.

When responding, ensure the generated code is in the correct programming language specified by the user. If no language is specified, ask for clarification.

"""

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=GENERATE_PROMPT),
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
    answer = await chain.ainvoke({"question": question, "chat_history": conversations})

    messages = [HumanMessage(content=state["question"]), AIMessage(content=answer)]
    return {"answer": answer, "messages": messages}
