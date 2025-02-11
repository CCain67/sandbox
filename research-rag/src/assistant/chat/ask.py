import openai

from assistant.config import (
    LLM,
    LLM_ROLE,
    OPENAI_API_KEY,
)
from assistant.vector_db.utils import get_qdrant_context


def ask(question: str) -> None:
    """Ask a question to the assistant."""
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    context = get_qdrant_context(question)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": LLM_ROLE,
                "content": "You are a helpful assistant knowledgeable about mathematics specializing in the intersection of manifolds, K-theory, and homotopy theory.",
            },
            {
                "role": "user",
                "content": f"""
            Here are some notes to help answer the question:
            {context}
            
            Question: {question}
            
            Please provide a detailed, clear explanation based on the provided notes.
            """,
            },
        ],
        model=LLM,
        stream=False,
    )

    print(chat_completion.choices[0].message.content)
