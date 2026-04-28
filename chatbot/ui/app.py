import streamlit as st
import uuid
import requests

API_URL = "http://localhost:9002/chat"  # FastAPI backend

st.set_page_config(page_title="Chatbot POC", layout="wide")

# ---------- State ----------
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session" not in st.session_state:
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = []
    st.session_state.current_session = session_id


# ---------- Sidebar (sessions) ----------
with st.sidebar:
    st.title("Sessions")

    if st.button("New Chat"):
        session_id = str(uuid.uuid4())
        st.session_state.sessions[session_id] = []
        st.session_state.current_session = session_id

    for sid in list(st.session_state.sessions.keys()):
        label = f"Chat {sid[:6]}"
        if st.button(label, key=sid):
            st.session_state.current_session = sid


# ---------- Chat Panel ----------
st.title("Chatbot")

session_id = st.session_state.current_session
messages = st.session_state.sessions[session_id]

# Display messages
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    try:
        response = requests.post(
            API_URL,
            json={
                "message": user_input,
                "session_id": session_id,
            },
            timeout=30,
        )
        data = response.json()
        bot_reply = data.get("response", "No response")

    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    # Save bot response
    messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)