"""
Configuration file for the project. Pulls OpenAI API key, 
fetches active Qdrant client, and defines an embedding model.
"""

import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

QDRANT_CLIENT = QdrantClient(url="http://localhost:6333")

EMBEDDING_MODEL = OpenAIEmbeddings(
    model="text-embedding-ada-002", api_key=OPENAI_API_KEY
)

# LLM = "o1-mini"  # gpt-4o
LLM = "gpt-4o"
LLM_ROLE = {
    "o1-mini": "assistant",
    "gpt-4o": "system",
}[LLM]
