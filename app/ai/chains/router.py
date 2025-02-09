from typing import Literal

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field

from app.ai.graph.state import GraphState
from app.ai.llms import openai_llm


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["generate", "review", "others"] = Field(
        ...,
        description="Given a user question choose to route it to generate or review or others.",
    )


def build_llm_router(state: GraphState):
    llm = openai_llm(state, False)
    structured_llm_router = llm.with_structured_output(RouteQuery)
    system = """
    You are an expert in routing user requests into one of three categories: 'generate', 'review', or 'others'.

    Analyze the user’s input to determine whether they are asking to generate new code or review existing code.
    If the request is for a code review, ensure that a code snippet is provided; otherwise, classify it as others.
    If the request is unclear, check the chat history for context.
    If no relevant context is found in the chat history or if the request does not match 'generate' or 'review,' classify it as 'others'.
    
    Return the classification as a string from: Literal["generate", "review", "others"].
    """

    route_prompt = ChatPromptTemplate(
        messages=[
            SystemMessage(content=system),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )
    question_router = route_prompt | structured_llm_router
    return question_router
