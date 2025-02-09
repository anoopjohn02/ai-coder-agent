from app.ai.chains.router import RouteQuery, build_llm_router
from app.ai.graph.consts import REVIEW, GENERATE, OTHERS
from app.ai.graph.state import GraphState
from app.services.conversation import get_messages_by_conversation_id


def route_question_node(state: GraphState) -> str:
    print("---ROUTE QUESTION---")
    question = state["question"]
    conversation_id = state["conversation_id"]
    conversations = get_messages_by_conversation_id(conversation_id)
    router = build_llm_router(state)
    source: RouteQuery = router.invoke({"question": question, "chat_history": [conversations]})
    if source.datasource == "generate":
        print("---ROUTE QUESTION TO GENERATE---")
        return GENERATE
    elif source.datasource == "review":
        print("---ROUTE QUESTION TO REVIEW---")
        return REVIEW
    elif source.datasource == "others":
        print("---ROUTE QUESTION TO OTHERS---")
        return OTHERS
    else:
        print("---NO MATCH - ROUTE QUESTION TO OTHERS---")
        return OTHERS
