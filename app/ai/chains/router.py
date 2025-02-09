from typing import Literal

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field

from app.ai.graph.state import GraphState
from app.ai.llms import default_llm


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["generate", "review", "others"] = Field(
        ...,
        description="Given a user question choose to route it to generate or review or others.",
    )


def build_llm_router(state: GraphState):
    llm = default_llm(state, False)
    structured_llm_router = llm.with_structured_output(RouteQuery)
    system = """You are an expert at routing a user question to a generate or review code.
    Read the question and identify the user ask to generate the code review the given code.
    When review the code the code snippet must given.
    If nothing is matching check chat history and find route.
    If chat history is empty or can't find anything use others.
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
