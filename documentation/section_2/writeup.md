# Writeup: Section 2 (LangChain RAG)

## FAISS vs Chroma
Both FAISS and Chroma are highly capable vector databases. 
- **Chroma** is generally preferred for extremely fast prototyping, in-memory ephemeral usage, and a frictionless developer experience without worrying about underlying algorithms.
- **FAISS**, developed by Facebook AI Research, shines in its massive scalability. It provides highly optimized C++ implementations for exact and approximate nearest neighbor search. It is significantly faster and more memory-efficient when dealing with millions of vectors in a production environment, especially because it supports both CPU and GPU (via CUDA) acceleration natively. 

In this section, we swapped to FAISS using the CPU version (`faiss-cpu`) to ensure compatibility across all testing environments while still keeping the semantic retrieval workflow identical to standard LangChain pipelines.

## Chunking Strategy
The data was chunked using the `RecursiveCharacterTextSplitter`. 
- **Chunk Size (200)**: A smaller chunk size ensures that the retrieved context is dense and highly relevant, minimizing token usage for the LLM. 
- **Chunk Overlap (20)**: Overlap prevents sentences or critical context from being cut in half across boundaries, preserving semantic meaning.

## Fallback Logic (Guardrails)
To prevent the LLM from hallucinating, we baked strict fallback logic directly into the `system_prompt`. If the retrieved documents from FAISS do not contain the answer, the LLM is explicitly instructed to refuse to answer by stating: *"I cannot answer this question based on the provided context."* This ensures the application behaves reliably and safely.
