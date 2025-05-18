from langchain_postgres import PGVector

from .state import State


class SearchCompentency:
    def __init__(self, compentency_store: PGVector):
        self.store = compentency_store

    def __call__(self, state: State):
        user_input = state["user_input"]
        retrieved_docs = self.store.similarity_search(
            user_input,
            k=5,
            filter={
                "$and": [
                    {
                        "sheet": {"$eq": "competencies"},
                    },
                    {
                        "model_name": {"$eq": state["embed_model_name"]},
                    },
                ]
            },
        )
        return {"competencies": retrieved_docs}
