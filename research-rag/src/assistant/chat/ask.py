import openai

from ..config import EMBEDDING_MODEL, OPENAI_API_KEY, QDRANT_CLIENT


def get_qdrant_context(query: str):
    """Get context from Qdrant based on a query."""
    query_vector = EMBEDDING_MODEL.embed_query(query)

    results = QDRANT_CLIENT.search(
        collection_name="personal_notes",
        query_vector=query_vector,
        limit=3,
    )

    context = "\n".join(
        [
            f"Context {i+1}: {result.payload['content']}"
            for i, result in enumerate(results)
        ]
    )
    return context


def ask(question: str) -> None:
    """Ask a question to the assistant."""
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    context = get_qdrant_context(question)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
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
        model="gpt-4o",
    )

    print(chat_completion.choices[0].message.content)
