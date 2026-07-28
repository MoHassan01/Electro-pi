# Section 3: Model Quantization Handover

## Overview
This section successfully implements a cross-platform benchmarking script that compares a large language model (`Qwen2.5-0.5B-Instruct`) in both full precision and 4-bit quantized formats.

## Key Engineering Decisions
1. **Model Selection**: Chosen `Qwen/Qwen2.5-0.5B-Instruct` as it provides excellent quality for a small parameter model while being perfectly sized to run inference on edge devices (Macbook Air) or free-tier compute without OOM errors or massive RAM overhead.
2. **Cross-Platform Compatibility**:
   - Instead of relying on `transformers` + PyTorch (which frequently causes `safetensors` multiprocessing deadlocks on MacOS/Python 3.13), the script was rewritten to use **GGUF for both Full Precision (FP16) and Quantization (Q4)**.
   - `llama.cpp` dynamically compiles and runs optimized C++ bindings across all major architectures (CUDA on Windows/Linux, Metal/MPS on Apple Silicon, and AVX on CPUs). By testing the FP16 `.gguf` weights against the Q4 `.gguf` weights natively, we get an absolute 1:1 hardware comparison without any PyTorch wrapper overhead or memory leak bugs.
3. **Benchmarking Loop**:
   - The script tracks memory via `psutil` (measuring the raw Resident Set Size increase after the model is loaded).
   - Throughput is calculated by explicitly timing the `generate` call and dividing the number of generated tokens by the duration.

## Current State
- The `quantize_benchmark.py` script is fully operational and requires no hardcoded paths or API keys.
- It iterates through 5 fixed prompts, proving the qualitative capabilities of both the full precision and 4-bit versions.
- It concludes by printing a summarized trade-off table.
