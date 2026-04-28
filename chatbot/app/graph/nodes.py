import json
from app.services.llm import call_llm
from app.services.mcp_client import list_tools, call_tool


from langchain_core.messages import AIMessage


async def agent_node(state):

    tools = await list_tools()

    llm_msg = call_llm(state["messages"], tools=tools)

    tool_calls = []

    if llm_msg.tool_calls:
        tool_calls = []

        if llm_msg.tool_calls:
            for tc in llm_msg.tool_calls:
                args = {}
                raw_args = tc.function.arguments

                if not raw_args:
                    args = {}

                elif isinstance(raw_args, str):
                    raw_args = raw_args.strip()

                    if raw_args == "":
                        args = {}
                    else:
                        args = json.loads(raw_args)

                elif isinstance(raw_args, dict):
                    args = raw_args

                else:
                    args = {}

                tool_calls.append({"name": tc.function.name, "args": args, "id": tc.id})

    return {
        "messages": [AIMessage(content=llm_msg.content or "", tool_calls=tool_calls)]
    }


def should_continue(state):
    last = state["messages"][-1]

    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"

    return "done"


from langchain_core.messages import ToolMessage


async def tool_node(state):

    last = state["messages"][-1]

    msgs = []

    for tc in last.tool_calls:

        try:
            result = await call_tool(tc["name"], tc["args"])
        except asyncio.TimeoutError:
            result = {"error": "Tool request timed out"}

        msgs.append(
            ToolMessage(
                content=json.dumps(result.data if hasattr(result, "data") else result),
                tool_call_id=tc["id"],
            )
        )

    return {"messages": msgs}
