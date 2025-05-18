import os
from typing import List
from uuid import uuid4

import pandas as pd
from langchain_core.documents import Document
from langchain_postgres import PGVector
from pandas import ExcelFile


class Store:
    def __init__(
        self,
        embed_model: any,
        connection_uri: str = "",
        competencies_collection_name: str = "",
        roles_collection_name: str = "",
        file_path: str = "",
    ) -> None:
        self.model = embed_model
        self.connection_uri = connection_uri or os.getenv("PGVECTOR_URI")
        if not self.connection_uri:
            raise ValueError(
                "Please specify `connection_uri` or set `PGVECTOR_URI` in environment variable."
            )
        self.competencies_collection_name = (
            competencies_collection_name or "competencies_docs"
        )
        self.roles_collection_name = roles_collection_name or "roles_docs"

        if not file_path:
            raise ValueError("Please specify `file_path`")
        self.file = pd.ExcelFile(file_path)

        self.competencies_store = PGVector(
            embeddings=self.model,
            collection_name=self.competencies_collection_name,
            connection=self.connection_uri,
            use_jsonb=True,
        )
        self.roles_store = PGVector(
            embeddings=self.model,
            collection_name=self.roles_collection_name,
            connection=self.connection_uri,
            use_jsonb=True,
        )
        self.cold_start()

    @staticmethod
    def process(
        file: ExcelFile, sheet_name: str, key: str, model_name: str
    ) -> List[Document]:
        df = file.parse(sheet_name)
        documents = []
        for _, row in df.iterrows():
            documents.append(
                Document(
                    page_content=row["description"],
                    metadata={
                        "id": str(uuid4()),
                        "sheet": sheet_name,
                        key: row[key],
                        "model_name": model_name,
                    },
                )
            )
        return documents

    @staticmethod
    def load(store: PGVector, documents: List[Document]) -> None:
        store.add_documents(documents, ids=[doc.metadata["id"] for doc in documents])

    @staticmethod
    def check(store: PGVector, model_name: str) -> bool:
        docs_in_store = store.similarity_search(
            "", filter={"model_name": {"$eq": model_name}}
        )
        return len(docs_in_store) != 0

    def cold_start(self) -> None:
        if not self.check(self.competencies_store, self.model.model):
            competencies_docs = self.process(
                self.file, "competencies", "competency", self.model.model
            )
            self.load(self.competencies_store, competencies_docs)
        if not self.check(self.roles_store, self.model.model):
            roles_docs = self.process(self.file, "roles", "role", self.model.model)
            self.load(self.roles_store, roles_docs)
