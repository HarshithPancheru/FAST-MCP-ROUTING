from fastapi import FastAPI
from app.models.schema import ChatRequest, ChatResponse
from app.graph.builder import build_graph

app = FastAPI()

graph = build_graph()


@app.post("/chat")
async def chat(req: ChatRequest):

    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": req.message}]},
        config={"configurable": {"thread_id": req.session_id}, "recursion_limit": 10},
    )

    final_message = result["messages"][-1].content
    return ChatResponse(response=final_message)
