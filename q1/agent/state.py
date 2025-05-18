from typing import Annotated, Dict, List, Sequence, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class State(TypedDict):
    user_input: str
    messages: Annotated[Sequence[BaseMessage], add_messages]
    competencies: List[Dict[str, str]]
    roles: List[Dict[str, str]]
    embed_model_name: str
