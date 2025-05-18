from langchain_postgres import PGVector

from .state import State


class SearchRole:
    def __init__(self, role_store: PGVector):
        self.store = role_store

    def __call__(self, state: State):
        user_input = state["user_input"]
        retrieved_docs = self.store.similarity_search(
            user_input,
            k=5,
            filter={
                "$and": [
                    {
                        "sheet": {"$eq": "roles"},
                    },
                    {
                        "model_name": {"$eq": state["embed_model_name"]},
                    },
                ]
            },
        )
        return {"roles": retrieved_docs}
