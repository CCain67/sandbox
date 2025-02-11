from langchain.agents import Tool

from assistant.chat.ask import get_qdrant_context

# Create a Tool instance for document search
search_tool = Tool(
    name="Document Search",
    func=get_qdrant_context,
    description="Use this tool to search for relevant passages in your document database.",
)
