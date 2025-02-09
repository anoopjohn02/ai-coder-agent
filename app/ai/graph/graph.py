from langgraph.graph import START, END, StateGraph

from .consts import GENERATE, OTHERS, HISTORY, REFINE, REVIEW
from .nodes import (route_question_node, generate_output_node, other_node,
                    save_history_node, refine_question_node, review_output_node)
from .state import GraphState

workflow = StateGraph(GraphState)

workflow.add_node(REFINE, refine_question_node)
workflow.add_node(GENERATE, generate_output_node)
workflow.add_node(REVIEW, review_output_node)
workflow.add_node(OTHERS, other_node)
workflow.add_node(HISTORY, save_history_node)

workflow.add_edge(START, REFINE)
workflow.add_conditional_edges(REFINE, route_question_node,
                               {
                                   REVIEW: REVIEW,
                                   GENERATE: GENERATE,
                                   OTHERS: OTHERS
                               })
workflow.add_edge(REVIEW, HISTORY)
workflow.add_edge(OTHERS, GENERATE)
workflow.add_edge(GENERATE, HISTORY)
workflow.add_edge(HISTORY, END)
graph = workflow.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
