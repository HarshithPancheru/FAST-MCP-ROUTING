import os
from dotenv import load_dotenv
from groq import Groq
import json

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "qwen/qwen3-32b"


SYSTEM_PROMPT = """
You are an enterprise facilities operations assistant.

You help users with:
- VDMS site operations
- IOC monitoring
- asset diagnostics
- alerts
- telemetry
- maintenance tickets
- energy and occupancy data

Tool usage rules:

1. ALWAYS inspect available tools before answering.
se ONLY tools explicitly provided in request.tools.

Never invent tool names.
Never modify tool names.
Never create new tools.

If needed functionality is unavailable,
tell you cannot do that task

2. If the request needs live operational data,
use the appropriate tool.

3. If the question is general knowledge or conversational,
answer directly without tools.

4. Never invent operational data.
If tool data is unavailable, say so.

5. If no tool matches the request,
say the available tools do not support that request.

6. After receiving tool output:
- interpret data
- summarise clearly
- mention issues, risks and observations
- make response user friendly
- do not dump raw JSON unless asked

7. For alerts/faults:
prioritize severity and mention impacted asset/site.

8. For asset telemetry:
highlight anomalies when values look abnormal.

9. Keep responses concise but useful.

10. If solving a question needs multiple tool calls,
perform them step by step.

11. Don't ever expose function calls, or other technical things to the end user

12. Use previous conversation context when resolving
references like:
- those assets
- that site
- them
- previous alerts

When using tools:
- choose the single best tool first
- do not call random tools
- use arguments carefully
"""


def to_openai_messages(messages):
    converted = []

    for m in messages:

        if isinstance(m, HumanMessage):
            converted.append({"role": "user", "content": m.content})

        elif isinstance(m, AIMessage):

            msg = {"role": "assistant", "content": m.content or ""}

            if getattr(m, "tool_calls", None):

                msg["tool_calls"] = []

                for tc in m.tool_calls:
                    msg["tool_calls"].append(
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": json.dumps(tc["args"]),
                            },
                        }
                    )

            converted.append(msg)

        elif isinstance(m, ToolMessage):
            converted.append(
                {"role": "tool", "tool_call_id": m.tool_call_id, "content": m.content}
            )

        else:
            converted.append(m)

    return converted


def call_llm(messages, tools=None):
    final_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + to_openai_messages(messages)

    params = {"model": MODEL, "messages": final_messages, "temperature": 0}

    if tools:
        params["tools"]=tools
    
        params["tool_choice"] = "auto"


    response = client.chat.completions.create(**params)

    return response.choices[0].message
