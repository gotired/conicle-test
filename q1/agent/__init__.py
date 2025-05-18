from typing import Any

from langchain_postgres import PGVector
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from .search_competency import SearchCompentency
from .search_role import SearchRole
from .state import State
from .summarize import Summarize


class Agent:
    def __init__(
        self, compentency_store: PGVector, role_store: PGVector, model: Any
    ) -> None:
        self.SearchCompentency = SearchCompentency(compentency_store=compentency_store)
        self.SearchRole = SearchRole(role_store=role_store)
        self.Summarize = Summarize(model=model)
        self.Graph = self.setup()

    def setup(self):
        graph_builder = StateGraph(State)
        graph_builder.add_node("RAGCompentency", self.SearchCompentency)
        graph_builder.add_node("RAGRole", self.SearchRole)
        graph_builder.add_node("Summarize", self.Summarize)

        graph_builder.add_edge(START, "RAGCompentency")
        graph_builder.add_edge(START, "RAGRole")
        graph_builder.add_edge("RAGCompentency", "Summarize")
        graph_builder.add_edge("RAGRole", "Summarize")
        graph_builder.add_edge("Summarize", END)

        memory = MemorySaver()
        graph = graph_builder.compile(checkpointer=memory)
        return graph
