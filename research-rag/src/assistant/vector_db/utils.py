"""Defines and checks the existence of collections in Qdrant."""

from uuid import uuid4

from langchain.schema import Document
from qdrant_client.http.models import VectorParams
from qdrant_client.models import PointStruct

from assistant.config import EMBEDDING_MODEL, QDRANT_CLIENT


def define_collection(collection_name: str, vector_size: int = 1536) -> None:
    """Create a Qdrant collection if it doesn't exist."""
    if not QDRANT_CLIENT.collection_exists(collection_name):
        QDRANT_CLIENT.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance="Cosine"),
        )
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")

    print("Collections:", QDRANT_CLIENT.get_collections())


def upsert_into_collection(
    documents: list[Document], vectors: list, collection_name: str
) -> None:
    """Upsert documents and vectors into a Qdrant collection."""

    points = [
        PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload={
                **doc.metadata,
                "content": doc.page_content,
            },
        )
        for (doc, vector) in zip(documents, vectors)
    ]

    QDRANT_CLIENT.upsert(collection_name=collection_name, points=points)


def query_collection(collection_name: str, query: str, limit: int = 3):
    """Query a Qdrant collection using a query string."""
    query_vector = EMBEDDING_MODEL.embed_query(query)

    results = QDRANT_CLIENT.search(
        collection_name=collection_name, query_vector=query_vector, limit=limit
    )

    return results


def get_qdrant_context(
    query: str, collection_name: str = "personal_notes", limit: int = 3
):
    """Get context from Qdrant based on a query."""
    results = query_collection(
        collection_name=collection_name, query=query, limit=limit
    )

    context = "\n".join(
        [
            f"Context {i+1}: {result.payload['content']}"
            for i, result in enumerate(results)
        ]
    )
    return context
