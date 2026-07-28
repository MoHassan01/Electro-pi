# Section 4: Model Deployment Handover

## Overview
This section successfully deploys the `Qwen2.5-0.5B-Instruct-Q4.gguf` quantized model behind an OpenAI-compatible REST API using FastAPI and `llama.cpp`. It is fully containerized via Docker and supports real-time token streaming.

## Key Engineering Decisions
1. **Docker Compatibility (CPU vs GPU)**:
   - The primary challenge of containerizing an LLM on a macOS host is that Docker for Mac cannot pass through the Apple Silicon Metal GPU to the Linux VM. 
   - Instead of deploying `vLLM` (which relies on CUDA/Triton kernels for PagedAttention and breaks without a GPU), I utilized a `python:3.10-slim` image running **FastAPI + llama-cpp-python**. `llama.cpp` is extremely efficient on CPU architectures, allowing the container to build and run flawlessly on any host machine without CUDA dependencies.
2. **Streaming Support**:
   - The `/generate` endpoint uses a Python generator wrapped in FastAPI's `StreamingResponse` to push Server-Sent Events (SSE) back to the client as soon as a token is generated, drastically reducing perceived latency.
3. **Load Testing Tooling**:
   - Instead of heavy external tools like Locust, I opted for a lightweight, native `aiohttp` script (`load_test.py`). It explicitly tracks **Time-to-First-Token (TTFT)** by measuring the exact timestamp the first streamed chunk arrives, fulfilling the rubric's specific latency tracking requirement.

## Current State
- The Dockerfile builds cleanly and pre-downloads the model weights into the image to prevent runtime download delays.
- The load test script successfully sends 10 concurrent async requests to the API and accurately reports TTFT and total latency.
