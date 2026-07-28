# Introduction to LLM Orchestration with LangChain

LangChain is a powerful framework designed to simplify the creation of applications using large language models.
One of its primary use cases is Retrieval-Augmented Generation (RAG). 

In RAG, LangChain is used to load documents, split them into smaller chunks, embed them using an embedding model like OpenAI's `text-embedding-ada-002`, and store them in a vector database like FAISS or Chroma.
When a user asks a question, the vector database is queried to find the most relevant chunks, which are then passed to the LLM to generate an accurate answer based on the retrieved context.
