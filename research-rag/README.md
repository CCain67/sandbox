# Research RAG

Qdrant + LangChain + GPT4o

## General Overview:
This RAG application sits on top of a Docker container running a [Qdrant](https://qdrant.tech/) vector database. The Docker image can be found here: https://hub.docker.com/r/qdrant/qdrant. I'm using OpenAIs `text-embedding-ada-002` text embedding model for vectorization, and 4o as the LLM. 

See also: https://platform.openai.com/docs/guides/embeddings

## Quick Conceptual notes:
- I'm choosing to vectorize my $\LaTeX$ notes as is - there is a lot of important contextual and semantic information in how the LaTex is formatted (for example, section headings give separation of concepts).
- For simplicity, and to keep this as a proof of concept, the $\LaTeX$ notes are written so that they are already in semantic chunks, broken up by new lines. There are plenty of other chunking methods you can use here for more intricate documents, see: https://www.wikiwand.com/en/articles/Retrieval-augmented_generation#Chunking

## Steps to run:
- First, sign up on OpenAI and generate an OpanAI API key. You'll need to add some money to your account for API calls, but it is not even remotely expensive (rates found here: https://openai.com/api/pricing/). I don't think I've even spent 5$ yet while creating and tinkering with this.
- Copy and paste your API key into a `.env` file containing:
```
OPENAI_API_KEY=sk-proj-aksjda12blahblah.......(rest of your API key)
```
- Start the Qdrant Docker container: if you are using VS Code, and you have the Docker extension installed, you can right-click the `docker-compose.yaml` file and select `Compose Up`, or if you have docker compose installed on your machine just navigate to the `.devcontainer` file in a terminal and run:
```
docker compose up
```
- From here you should see the Qdrant ASCII art in the terminal giving you a link (http://localhost:6333/dashboard) to the web UI.
- The `lab.ipynb` notebook gives examples how to use the functions I wrote to create Qdrant collections, vectorize documents and store them in Qdrant.