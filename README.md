# Electro Pi AI Engineer Test Overview

The Electro Pi AI Engineer Technical Test evaluates practical skills in building AI applications.
It is divided into 4 main sections:
1. LiveKit Agents
2. LangChain (RAG)
3. Quantization
4. Model Deployment

## Repository Structure
- **`section_1/`**: LiveKit Voice Agent implementation with tool-calling functionality.
- **`section_2/`**: LangChain Retrieval-Augmented Generation (RAG) pipeline over sample documents.
- **`section_3/`**: LLM Quantization evaluation (Full precision vs 4-bit).
- **`section_4/`**: FastAPI Model Deployment with Docker and asynchronous streaming.
- **`documentation/`**: Step-by-step handover documents and technical write-ups for each section.

---

## Global Setup (Virtual Environment)

To prevent package conflicts, it is highly recommended to use a Python virtual environment to run these tasks. 

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

## 1. Section 1 (LiveKit Agents)

This section contains a minimal voice assistant (built with LiveKit's new v1.6 AgentServer architecture) that connects to a room and provides food delivery support using a tool call (`get_order_status`).

### Prerequisites & API Keys
You will need three sets of free API keys for this section:
1. **Google (Gemini) API Key** (for the LLM): Get it from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. **Deepgram API Key** (for STT and TTS): Get it from the [Deepgram Console](https://console.deepgram.com/).
3. **LiveKit Cloud Keys**: Sign in to [LiveKit Cloud](https://cloud.livekit.io/), create a project, and go to **Project Settings -> Keys** to get your URL, API Key, and API Secret.

### Setup and Execution
1. Navigate into the `section_1` directory:
   ```bash
   cd section_1
   ```

2. Install the necessary dependencies:
   ```bash
   pip install livekit-agents livekit-plugins-google livekit-plugins-deepgram livekit-plugins-silero python-dotenv
   ```

3. Create a file named `.env.local` inside the `section_1` directory, and paste in your keys:
   ```env
   GOOGLE_API_KEY="your-google-api-key"
   DEEPGRAM_API_KEY="your-deepgram-api-key"
   LIVEKIT_URL="wss://your-project.livekit.cloud"
   LIVEKIT_API_KEY="your-livekit-api-key"
   LIVEKIT_API_SECRET="your-livekit-api-secret"
   ```

4. Start the agent:
   ```bash
   python agent.py start
   ```
   *(To stop the agent cleanly, press `Ctrl+C` in your terminal)*

### How to Test
Once the agent says "registered worker" in your terminal, navigate to the **Sandbox** in your LiveKit Cloud dashboard. Connect to the room and start speaking. Try asking: *"Can you check the status of my order? The ID is 456."*

*See `documentation/section_1/writeup.md` for thoughts on barge-in and tool safety, and `documentation/section_1/handover.md` for steps taken.*

---

## 2. Section 2 (LangChain RAG)

This section demonstrates a Retrieval-Augmented Generation (RAG) pipeline using **FAISS**, **HuggingFace Embeddings** (run locally), and **Google Gemini** (via API). It is configured with strict fallback guardrails to prevent hallucination.

### Prerequisites & API Keys
1. **HuggingFace Access Token**: A free HuggingFace account token is required for the LLM endpoint (`HF_TOKEN`). No paid APIs are required.

### Setup and Execution
1. Navigate into the `section_2` directory:
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

### How to Test
When you run the script, it will:
1. Load dummy markdown documents from `section_2/sample_docs/`.
2. Chunk them using `RecursiveCharacterTextSplitter`.
3. Clear any existing `faiss_index/` directory and build a fresh FAISS vectorstore locally.
4. Sample the first generated vector (printing its metadata and first 5 dimensions).
5. Invoke three queries against the RAG chain using the HuggingFace Mistral API.
   - The first two questions should answer accurately based on the docs.
   - The third question ("Who won the world cup in 2022?") should trigger the strict fallback guardrail: *"I cannot answer this question based on the provided context."*

*See `documentation/section_2/writeup.md` for technical thoughts, and `documentation/section_2/handover.md` for steps taken.*

---

## 3. Section 3 (Quantization)

This section demonstrates running a local open-weights LLM (`Qwen2.5-0.5B-Instruct`) in both **full precision (fp16/bf16)** and **4-bit quantization (GGUF via llama.cpp)**. 
It features a complete benchmarking loop that measures memory footprint (RAM/VRAM), tokens/sec throughput, and qualitative output across 5 fixed prompts to create a final trade-off table.

### Cross-Platform Hardware Routing
The script is explicitly designed for flawless multi-platform execution:
1. **Full Precision Benchmark (FP16)**: Downloads `Qwen2.5-0.5B-Instruct-FP16.gguf` and runs it natively via `llama.cpp`. This bypasses a known PyTorch memory-mapping deadlock on Apple Silicon while still testing true full-precision weights.
2. **Quantized Benchmark (Q4)**: Downloads `Qwen2.5-0.5B-Instruct-Q4.gguf` and runs it using the exact same `llama.cpp` pipeline.
3. Both benchmarks natively compile and route to CUDA (Windows/Linux) or Metal (MacOS).

### Setup and Execution
1. Navigate into the `section_3` directory:
   ```bash
   cd section_3
   ```

2. Install the necessary dependencies (assuming your `.venv` is activated):
   - **For Windows / Linux**:
     ```bash
     pip install transformers accelerate torch psutil huggingface-hub llama-cpp-python
     ```
   - **For Mac (Apple Silicon)**: 
     *(This ensures llama.cpp compiles with Metal GPU acceleration)*
     ```bash
     CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python transformers accelerate torch psutil huggingface-hub
     ```

3. Run the benchmark:
   ```bash
   python quantize_benchmark.py
   ```

### How to Test
1. The script will first download the full-precision `Qwen2.5-0.5B-Instruct` model and run 5 prompts, tracking memory and speed.
2. Next, it will download the quantized `Qwen2.5-0.5B-Instruct-GGUF` model and run the exact same 5 prompts.
3. At the end, it will print a markdown table comparing the Size, Speed, and Memory Footprint trade-offs.

---

## 4. Section 4 (Model Deployment)

This section deploys the quantized LLM behind a production-ready REST API using **FastAPI** and **Docker**. It natively supports response streaming and includes an asynchronous load-testing script to measure concurrent latency.

### The Docker Mac Constraint
While frameworks like `vLLM` are incredible for high-throughput GPU environments, Docker on macOS runs inside a Linux VM that **cannot access the Apple Metal GPU**. To ensure this Docker container runs flawlessly on any reviewer's machine, the API wraps the C++ based `llama.cpp` engine, which is universally stable on CPUs.

### Setup and Execution

1. Navigate to the `section_4` directory:
   ```bash
   cd section_4
   ```

2. **Build the Docker Image**:
   *Note: This will take a few minutes as it compiles C++ binaries and pre-downloads the model weights directly into the image.*
   ```bash
   docker build -t qwen-api .
   ```

3. **Run the Docker Container**:
   ```bash
   docker run -p 8000:8000 qwen-api
   ```
   *The server is now live at `http://localhost:8000`.*

### Testing and Benchmarking

To test the API and measure the required concurrent load/latency metrics, open a **new terminal tab**, activate your python virtual environment, and run the load test:
```bash
cd section_4
python load_test.py
```

The script will fire 10 concurrent requests to the API and measure the **Time-to-First-Token (TTFT)** and total latency for each request.
