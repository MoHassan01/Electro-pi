# Section 2: LangChain RAG

This section demonstrates a Retrieval-Augmented Generation (RAG) pipeline using **FAISS**, **HuggingFace Embeddings** (run locally), and **Google Gemini** (via API). It is configured with strict fallback guardrails to prevent hallucination.

## Prerequisites & API Keys
1. **HuggingFace Access Token**: A free HuggingFace account token is required for the LLM endpoint (`HF_TOKEN`). No paid APIs are required.

## Setup and Execution
1. Navigate into the `section_2` directory (if not already there):
   ```bash
   cd section_2
   ```

2. Install the necessary dependencies (assuming your `.venv` is activated):
   ```bash
   pip install langchain langchain-google-genai langchain-community langchain-huggingface sentence-transformers faiss-cpu
   ```

3. Export your HuggingFace Token to your terminal session:
   - On macOS/Linux: `export HF_TOKEN="your-hf-token"`
   - On Windows: `set HF_TOKEN="your-hf-token"`

4. Run the pipeline:
   ```bash
   python rag_pipeline.py
   ```

## How to Test
When you run the script, it will:
1. Load dummy markdown documents from `sample_docs/`.
2. Chunk them using `RecursiveCharacterTextSplitter`.
3. Clear any existing `faiss_index/` directory and build a fresh FAISS vectorstore locally.
4. Sample the first generated vector (printing its metadata and first 5 dimensions).
5. Invoke three queries against the RAG chain using the HuggingFace Mistral API.
   - The first two questions should answer accurately based on the docs.
   - The third question ("Who won the world cup in 2022?") should trigger the strict fallback guardrail: *"I cannot answer this question based on the provided context."*

*See `../documentation/section_2/writeup.md` for technical thoughts, and `../documentation/section_2/handover.md` for steps taken.*
