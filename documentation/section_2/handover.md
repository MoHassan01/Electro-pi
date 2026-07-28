# Handover: Section 2 (LangChain RAG)

## Task Requirements
Build a Retrieval-Augmented Generation (RAG) pipeline utilizing FAISS and LangChain over sample documents. The task specifically requires adapting the workflow to use free local embeddings (HuggingFace) and implementing a strict fallback guardrail to prevent hallucination.

## Steps Taken
1. **Created `rag_pipeline.py`**:
   - Initialized a RAG pipeline utilizing `DirectoryLoader` to read markdown documents from the `sample_docs/` folder.
   - Set up text chunking using `RecursiveCharacterTextSplitter`.
   - Utilized completely free and local embeddings via `HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")`.
   - Configured FAISS to automatically rebuild the vectorstore if it already exists, and saved the vectorstore to a local `faiss_index/` directory.
   - Added the `sampling_vector` logic directly from the reference article to print vector metadata and the first 5 dimensionality values.
   - Connected the FAISS retriever to a free HuggingFace LLM Endpoint (`zephyr-7b-beta`) using a custom system prompt that forces a fallback response if the answer isn't in the context.

2. **Provided Sample Docs**:
   - Created `sample_docs/` populated with `doc1.md` and `doc2.md` containing mock knowledge base information.

3. **Created `writeup.md`**:
   - Detailed the comparison between FAISS and Chroma, and explained the chunking and fallback strategies.

## How to Test
1. Set up your virtual environment and install dependencies: `pip install langchain langchain-google-genai langchain-community langchain-huggingface sentence-transformers faiss-cpu`
2. Export your HuggingFace Token: `export HF_TOKEN="your-api-key"`
3. Run the pipeline: `python rag_pipeline.py`
4. The output will demonstrate the FAISS index creation, vector sampling, successful QA retrieval, and a successful guardrail rejection for off-topic queries.
