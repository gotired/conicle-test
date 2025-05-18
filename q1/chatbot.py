from typing import Any
from uuid import uuid4

import pandas as pd
import requests
import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings

from agent import Agent
from store import Store


class Chatbot:
    def __init__(
        self,
        chat_model_name: Any,
        embed_model_name: Any,
        connection_uri: str = "",
        competencies_collection_name: str = "",
        roles_collection_name: str = "",
        file_path: str = "",
        base_url: str = "http://ollama:11434",
        chat_model_temp: float = 0.5,
    ):
        self.base_url = base_url
        self.download(model_name=chat_model_name, base_url=base_url)
        self.model = ChatOllama(
            model=chat_model_name, temperature=chat_model_temp, base_url=base_url
        )
        self.download(model_name=embed_model_name, base_url=base_url)
        self.embed_model = OllamaEmbeddings(model=embed_model_name, base_url=base_url)
        self.embed_model_name = embed_model_name

        self.store_service = Store(
            embed_model=self.embed_model,
            connection_uri=connection_uri,
            competencies_collection_name=competencies_collection_name,
            roles_collection_name=roles_collection_name,
            file_path=file_path,
        )
        ai = Agent(
            compentency_store=self.store_service.competencies_store,
            role_store=self.store_service.roles_store,
            model=self.model,
        )
        self.graph = ai.Graph

    async def stream_response(self, prompt: str, reasoning_model: bool = False):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        full_response = ""
        with st.chat_message("assistant"):
            competencies_slot = st.empty()
            roles_slot = st.empty()
            thinking_slot = st.empty()
            message_placeholder = st.empty()
            thinking_expander = think_placeholder = None
            buffer = ""
            in_think, think_ended = False, False
            think_collected = ""
            competencies_expander = competencies_placeholder = None
            roles_expander = roles_placeholder = None
            roles_collected = competencies_collected = ""

            config = {"configurable": {"thread_id": uuid4()}}
            input_message = {
                "user_input": prompt,
                "embed_model_name": self.embed_model_name,
            }

            async for mes in self.graph.astream_events(
                input_message, version="v2", config=config
            ):
                event = mes["event"]
                name = mes.get("name")

                if event != "on_chat_model_stream":
                    if event == "on_chain_end":
                        output = mes["data"]["output"]
                        if name == "RAGCompentency":
                            competencies_df = pd.DataFrame(
                                [
                                    {
                                        "competency": doc.metadata["competency"],
                                        "description": doc.page_content,
                                    }
                                    for doc in output["competencies"]
                                ]
                            )
                            competencies_collected = competencies_df.to_markdown()
                            if not competencies_expander:
                                with competencies_slot.container():
                                    competencies_expander = st.expander(
                                        "Related Competencies", expanded=True
                                    )
                                    competencies_placeholder = (
                                        competencies_expander.empty()
                                    )
                                competencies_placeholder.markdown(
                                    competencies_collected
                                )
                        elif name == "RAGRole":
                            roles_df = pd.DataFrame(
                                [
                                    {
                                        "role": doc.metadata["role"],
                                        "description": doc.page_content,
                                    }
                                    for doc in output["roles"]
                                ]
                            )
                            roles_collected = roles_df.to_markdown()
                            if not roles_expander:
                                with roles_slot.container():
                                    roles_expander = st.expander(
                                        "Related Roles", expanded=True
                                    )
                                    roles_placeholder = roles_expander.empty()
                                roles_placeholder.markdown(roles_collected)
                    continue

                chunk = mes["data"]["chunk"].content
                buffer += chunk

                while buffer:
                    if reasoning_model and not think_ended:
                        start_idx = buffer.find("<think>")
                        end_idx = buffer.find("</think>")

                        if not in_think and start_idx != -1:
                            buffer = buffer[start_idx + len("<think>") :]
                            in_think = True
                            if not thinking_expander:
                                with thinking_slot.container():
                                    thinking_expander = st.expander(
                                        "🤔 Thinking...", expanded=True
                                    )
                                    think_placeholder = thinking_expander.empty()
                                think_placeholder.markdown(think_collected)

                        elif in_think and end_idx != -1:
                            think_collected += buffer[:end_idx]
                            buffer = buffer[end_idx + len("</think>") :]
                            think_placeholder.markdown(think_collected + "▌")
                            in_think = False
                            think_ended = True
                            continue

                        elif in_think:
                            think_collected += buffer
                            buffer = ""
                            think_placeholder.markdown(think_collected + "▌")
                            break
                        else:
                            buffer = ""
                            break
                    else:
                        full_response += buffer
                        buffer = ""
                        message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": full_response}
        )

    @staticmethod
    def download(model_name: str, base_url: str = "http://ollama:11434"):
        response = requests.post(
            f"{base_url}/api/pull", json={"model": model_name, "stream": False}
        )
        response_json = response.json()
        if response_json["status"] != "success":
            raise Exception(f"Download model {model_name} error.")
