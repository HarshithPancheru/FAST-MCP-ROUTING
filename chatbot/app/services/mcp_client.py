from fastmcp import Client
import os
from dotenv import load_dotenv

load_dotenv()

MCP_URL = os.getenv("MCP_URL")


async def list_tools():
    async with Client(MCP_URL) as client:
        tools = await client.list_tools()

        formatted = []

        for t in tools:
            formatted.append(
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema
                    }
                }
            )

        return formatted


async def call_tool(name, args):
    async with Client(MCP_URL) as client:
        result = await client.call_tool(
            name,
            arguments=args
        )

        return result