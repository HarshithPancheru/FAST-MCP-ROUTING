```bash
uvicorn server:app --reload --port 9001
fastmcp run server.py:mcp --transport http --port 8000
uvicorn app.main:app --reload --port 9002
streamlit run app.py
```