from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.graph.nodes import agent_node, tool_node, should_continue

from app.graph.state import AgentState


def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node("agent", agent_node)

    builder.add_node("tool", tool_node)

    builder.set_entry_point("agent")

    builder.add_conditional_edges(
        "agent", should_continue, {"tools": "tool", "done": END}
    )

    builder.add_edge("tool", "agent")

    memory = MemorySaver()

    return builder.compile(checkpointer=memory)
