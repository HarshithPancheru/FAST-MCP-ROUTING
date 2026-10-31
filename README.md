# FAST-MCP-ROUTING

A building intelligence chatbot that uses **FastMCP, LangGraph, and FastAPI** to retrieve and analyze building property information through an MCP-based tool integration.

The project demonstrates how an AI-powered chatbot can interact with external services through the Model Context Protocol (MCP). Users can interact with the chatbot through a browser-based interface and ask questions to gain insights about different buildings.

The system consists of three independent services: a mock Building Property Server, an MCP Server, and a Chatbot Server (MCP Client).

## Architecture

The project is divided into three main services:

### 1. Building Property Server

A mock backend service that exposes building-related information through HTTP APIs.

- Built using FastAPI (Python).
- Provides endpoints to retrieve building properties and information.
- Uses static mock data stored in JSON files.
- Does not use a database.
- Acts as the data source for the MCP Server.

### 2. MCP Server

An MCP server that exposes building property operations as tools that AI agents can consume.

- Built using FastAPI and FastMCP.
- Defines tools based on the operations exposed by the Building Property Server.
- Fetches building information by communicating with the actual property server.
- Exposes building-related tools through the Model Context Protocol.
- Acts as an abstraction layer between the chatbot and the underlying property service.

### 3. Chatbot Server (MCP Client)

The chatbot server acts as an MCP client and provides the conversational intelligence.

- Built using FastAPI (Python).
- Uses LangGraph to orchestrate the chatbot workflow.
- Connects to the MCP Server and discovers its available tools.
- Invokes MCP tools based on user queries.
- Supports recursive tool invocation, allowing the agent to make additional tool calls when required to gather information.
- Processes retrieved building information and generates contextual responses.

## User Interface

The project uses **Streamlit** to provide a browser-based chatbot interface.

Users can:
- Interact with the chatbot using natural language.
- Ask questions about different buildings.
- Retrieve building property information.
- Request insights based on available building data.
- Ask follow-up questions within the conversation.

### Request Flow

1. The user submits a question through the Streamlit interface.
2. The chatbot server receives the request.
3. LangGraph processes the conversation and determines whether external building information is required.
4. The chatbot invokes the appropriate tools exposed by the MCP Server.
5. The MCP Server communicates with the Building Property Server to retrieve the requested information.
6. The MCP Server returns the tool results to the chatbot.
7. LangGraph can recursively invoke additional tools when more information is required.
8. The chatbot processes the collected information and generates a response.
9. The response is displayed to the user through Streamlit.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| API Framework | FastAPI |
| MCP Implementation | FastMCP |
| AI Workflow Orchestration | LangGraph |
| MCP Communication | Model Context Protocol |
| User Interface | Streamlit |
| Mock Data Storage | JSON |
| Architecture | Microservices |

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- API key for the configured LLM provider

### Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:HarshithPancheru/FAST-MCP-ROUTING.git
   ```

2. Navigate to the project directory:

   ```bash
   cd FAST-MCP-ROUTING
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows:

   ```bash
   venv\Scripts\activate
   ```

   Linux / macOS:

   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Configure the required environment variables, including the LLM provider API key and service URLs.

### Running the Application

Start all three FastAPI services independently.

**1. Building Property Server**

```bash
uvicorn server:app --reload --port 9001
```

**2. MCP Server**

```bash
fastmcp run server.py:mcp --transport http --port 8000
```

**3. Chatbot Server**

```bash
uvicorn app.main:app --reload --port 9002
```

**4. Streamlit UI**

```bash
streamlit run app.py
```

*Update the commands, ports, and working directories according to your actual configuration.*

## Key Concepts Demonstrated

This project explores the integration of AI agents with external services using the Model Context Protocol.

- **Model Context Protocol (MCP):** Exposing external service functionality as tools that AI agents can discover and invoke.
- **FastMCP:** Defining and exposing MCP tools using Python.
- **LangGraph:** Orchestrating agent workflows and managing tool execution.
- **Recursive Tool Invocation:** Allowing the chatbot to perform multiple tool calls to gather information before generating a response.
- **Service Integration:** Connecting independently running FastAPI services through HTTP and MCP communication.
- **Tool Abstraction:** Separating the underlying property data source from the AI agent through an MCP layer.

## Purpose

The primary objective of this project is to explore how MCP can be used to connect AI agents with external services and structured data sources.

It demonstrates a modular architecture where:
- The property server owns and exposes the actual building data.
- The MCP server converts property operations into reusable AI-accessible tools.
- The chatbot server uses LangGraph to orchestrate tool discovery, execution, and response generation.
- The Streamlit interface provides a simple way for users to interact with the system.

## Future Enhancements

- Integrate a persistent database instead of static JSON data.
- Support additional property-related services.
- Introduce more advanced building analytics.
- Improve multi-agent orchestration and tool selection.
- Add authentication and access control.
- Support additional MCP-connected data sources.


