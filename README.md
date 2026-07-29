# Electro Pi AI Engineer Test Overview

The Electro Pi AI Engineer Technical Test evaluates practical skills in building AI applications. This repository contains the implementations for four distinct technical challenges, demonstrating capabilities across voice agents, RAG, model quantization, and API deployment.

## Sections & Challenges

1. **[Section 1: LiveKit Agents](./section_1/README.md)**
   A minimal voice assistant built with LiveKit's v1.6 AgentServer architecture. It connects to a room and provides food delivery support using a function tool call (`get_order_status`).

2. **[Section 2: LangChain RAG](./section_2/README.md)**
   A Retrieval-Augmented Generation (RAG) pipeline utilizing FAISS, local HuggingFace embeddings, and Google Gemini. Configured with strict fallback guardrails to prevent hallucination.

3. **[Section 3: Quantization](./section_3/README.md)**
   A local benchmarking script that compares `Qwen2.5-0.5B-Instruct` in both full precision (FP16) and 4-bit quantization (GGUF via llama.cpp). Evaluates memory footprint, tokens/sec throughput, and qualitative output.

4. **[Section 4: Model Deployment](./section_4/README.md)**
   A production-ready REST API using FastAPI and Docker to deploy the quantized LLM. Natively supports response streaming and includes an asynchronous load-testing script to measure concurrent latency.

## Repository Structure
- **`section_1/`**: LiveKit Voice Agent implementation.
- **`section_2/`**: LangChain RAG pipeline.
- **`section_3/`**: LLM Quantization benchmarking.
- **`section_4/`**: FastAPI Model Deployment.
- **`documentation/`**: Step-by-step handover documents and technical write-ups for each section.

---

## Global Setup (Virtual Environment)

To prevent package conflicts, it is highly recommended to use a Python virtual environment to run these tasks. Detailed setup and execution instructions are available within each section's respective `README.md`.

1. **Clone the repository and enter the directory**:
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. **Create a Python 3.10+ virtual environment** (using `uv` or `venv`):
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux: `source .venv/bin/activate`
   - On Windows: `.venv\Scripts\activate`

*Note: Ensure your virtual environment is active before installing the dependencies for each section.*

---

**Explore each section directory for detailed setup instructions, test procedures, and implementation notes.**
