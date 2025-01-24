"""Vectorize LaTeX content and load into Qdrant"""

from langchain.schema import Document

from ..config import EMBEDDING_MODEL


def chunkify(path: str) -> list[str]:
    """Chunkify a LaTeX file into paragraphs."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return content.split("\n\n")


def generate_embeddings(latex_code: list[str], filename: str) -> list[Document]:
    """Generate embeddings for LaTeX code chunks."""
    documents = [
        Document(
            page_content=chunk,
            metadata={"filename": filename, "chunk_index": idx},
        )
        for idx, chunk in enumerate(latex_code)
    ]
    vectors = [EMBEDDING_MODEL.embed_query(doc.page_content) for doc in documents]
    return documents, vectors
