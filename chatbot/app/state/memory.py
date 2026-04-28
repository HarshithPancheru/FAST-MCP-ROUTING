store = {}

def get_history(session_id: str):
    return store.get(session_id, [])

def add_message(session_id: str, role: str, content: str):
    if session_id not in store:
        store[session_id] = []
    store[session_id].append({"role": role, "content": content})