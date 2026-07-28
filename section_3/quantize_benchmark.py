import os
import time
import psutil
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
GGUF_REPO_ID = "Qwen/Qwen2.5-0.5B-Instruct-GGUF"
GGUF_FP16_FILENAME = "qwen2.5-0.5b-instruct-fp16.gguf"
GGUF_Q4_FILENAME = "qwen2.5-0.5b-instruct-q4_k_m.gguf"

PROMPTS = [
    "Explain the theory of relativity in one simple sentence.",
    "Write a short haiku about artificial intelligence.",
    "What is the capital of France, and why is it famous?",
    "Give me a 3-step plan to learn Python.",
    "Why is the sky blue? Answer like a pirate."
]

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def get_memory_usage_mb():
    """Returns the current process memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def print_header(title):
    print(f"\n{'='*60}\n{title}\n{'='*60}")

def run_benchmark(filename, title):
    print_header(title)
    
    print(f"Downloading/Locating {filename} from HuggingFace Hub...")
    gguf_path = hf_hub_download(repo_id=GGUF_REPO_ID, filename=filename)
    
    print(f"Loading {filename} via Llama.cpp natively...")
    
    baseline_mem = get_memory_usage_mb()
    
    # n_gpu_layers=-1 delegates all layers to the GPU (CUDA/Metal) if available
    llm = Llama(
        model_path=gguf_path,
        n_gpu_layers=-1,
        verbose=False, # Suppress the huge C++ logs
        n_ctx=2048
    )
    
    loaded_mem = get_memory_usage_mb()
    memory_footprint = loaded_mem - baseline_mem
    print(f"Memory Footprint ({title}): {memory_footprint:.2f} MB")
    
    total_tokens = 0
    total_time = 0.0

    print("\n--- Running Inference ---")
    for i, prompt in enumerate(PROMPTS):
        start_time = time.time()
        
        output = llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        
        end_time = time.time()
        
        response = output['choices'][0]['message']['content']
        num_tokens = output['usage']['completion_tokens']
        duration = end_time - start_time
        
        total_time += duration
        total_tokens += num_tokens
        
        print(f"\n[Prompt {i+1}]: {prompt}")
        print(f"[Response]: {response.strip()}")
        print(f"[Stats]: {num_tokens} tokens generated in {duration:.2f}s ({num_tokens/duration:.2f} tokens/sec)")

    avg_tps = total_tokens / total_time
    print(f"\nAverage Throughput ({title}): {avg_tps:.2f} tokens/sec")
    
    # Free memory
    del llm
    return {"memory_mb": memory_footprint, "avg_tps": avg_tps}

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    print_header("ELECTRO PI - SECTION 3 (QUANTIZATION BENCHMARK)")
    print("This script will run Qwen2.5-0.5B in Full Precision (FP16 GGUF), followed by 4-bit Quantized (Q4 GGUF).")
    print("It uses llama.cpp to ensure rock-solid stability and native GPU acceleration (CUDA/Metal) across all OSs.")
    
    # 1. Run Full Precision
    fp_stats = run_benchmark(GGUF_FP16_FILENAME, "1. FULL PRECISION BENCHMARK (FP16)")
    
    # 2. Run Quantized
    q_stats = run_benchmark(GGUF_Q4_FILENAME, "2. QUANTIZED BENCHMARK (4-Bit)")
    
    # 3. Print Final Trade-off Table
    print_header("3. TRADE-OFF SUMMARY")
    print("| Metric | Full Precision (FP16) | Quantized (4-Bit GGUF) |")
    print("|--------|-----------------------|------------------------|")
    print(f"| Memory | {fp_stats['memory_mb']:.2f} MB | {q_stats['memory_mb']:.2f} MB |")
    print(f"| Speed  | {fp_stats['avg_tps']:.2f} tokens/sec | {q_stats['avg_tps']:.2f} tokens/sec |")
    print("| Quality| (See Console Logs)    | (See Console Logs)     |")
    
    print("\nBenchmark Complete!")
