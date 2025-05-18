import asyncio
import os

import streamlit as st

from chatbot import Chatbot

ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

# If we use reasoning model set `REASON_MODEL_FLAG` to be true for example model "deepseek-r1:1.5b"
reasoning_model = os.getenv("REASON_MODEL_FLAG", "false").lower() == "true"
chat_model_name = os.getenv("CHAT_MODEL", "gemma3:1b")
embed_model_name = os.getenv("EMBED_MODEL", "nomic-embed-text")


chatbot = Chatbot(
    chat_model_name=chat_model_name,
    embed_model_name=embed_model_name,
    file_path="./data/openai_result.xlsx",
    base_url=ollama_base_url,
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.title("Courses recommendation")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Enter a competency name or description...")
if user_input:
    with st.spinner("Thinking..."):
        asyncio.run(
            chatbot.stream_response(prompt=user_input, reasoning_model=reasoning_model)
        )
