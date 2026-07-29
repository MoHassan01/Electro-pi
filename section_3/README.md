# Section 3: Quantization

This section demonstrates running a local open-weights LLM (`Qwen2.5-0.5B-Instruct`) in both **full precision (fp16/bf16)** and **4-bit quantization (GGUF via llama.cpp)**. 
It features a complete benchmarking loop that measures memory footprint (RAM/VRAM), tokens/sec throughput, and qualitative output across 5 fixed prompts to create a final trade-off table.

## Cross-Platform Hardware Routing
The script is explicitly designed for flawless multi-platform execution:
1. **Full Precision Benchmark (FP16)**: Downloads `Qwen2.5-0.5B-Instruct-FP16.gguf` and runs it natively via `llama.cpp`. This bypasses a known PyTorch memory-mapping deadlock on Apple Silicon while still testing true full-precision weights.
2. **Quantized Benchmark (Q4)**: Downloads `Qwen2.5-0.5B-Instruct-Q4.gguf` and runs it using the exact same `llama.cpp` pipeline.
3. Both benchmarks natively compile and route to CUDA (Windows/Linux) or Metal (MacOS).

## Setup and Execution
1. Navigate into the `section_3` directory (if not already there):
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

## How to Test
1. The script will first download the full-precision `Qwen2.5-0.5B-Instruct` model and run 5 prompts, tracking memory and speed.
2. Next, it will download the quantized `Qwen2.5-0.5B-Instruct-GGUF` model and run the exact same 5 prompts.
3. At the end, it will print a markdown table comparing the Size, Speed, and Memory Footprint trade-offs.

*See `../documentation/section_3/writeup.md` for technical thoughts, and `../documentation/section_3/handover.md` for steps taken.*
