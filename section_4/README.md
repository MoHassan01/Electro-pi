# Section 4: Model Deployment

This section deploys the quantized LLM behind a production-ready REST API using **FastAPI** and **Docker**. It natively supports response streaming and includes an asynchronous load-testing script to measure concurrent latency.

## The Docker Mac Constraint
While frameworks like `vLLM` are incredible for high-throughput GPU environments, Docker on macOS runs inside a Linux VM that **cannot access the Apple Metal GPU**. To ensure this Docker container runs flawlessly on any reviewer's machine, the API wraps the C++ based `llama.cpp` engine, which is universally stable on CPUs.

## Setup and Execution

1. Navigate to the `section_4` directory (if not already there):
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

## Testing and Benchmarking

To test the API and measure the required concurrent load/latency metrics, open a **new terminal tab**, activate your python virtual environment, and run the load test:
```bash
cd section_4
python load_test.py
```

The script will fire 10 concurrent requests to the API and measure the **Time-to-First-Token (TTFT)** and total latency for each request.

*See `../documentation/section_4/writeup.md` for technical thoughts, and `../documentation/section_4/handover.md` for steps taken.*
