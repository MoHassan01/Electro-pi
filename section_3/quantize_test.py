import time
import psutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# Note: This script is intended to be run on a system with a CUDA-compatible GPU.
# To run successfully, you need: pip install transformers accelerate bitsandbytes torch

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"

PROMPTS = [
    "Explain the concept of RAG in one short paragraph.",
    "Write a Python function to compute the Fibonacci sequence.",
    "What is the capital of France?",
    "Summarize the plot of the Matrix movie in 2 sentences.",
    "Translate 'Hello, how are you?' to Spanish."
]

def print_memory_usage():
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / (1024**3)
        reserved = torch.cuda.memory_reserved() / (1024**3)
        print(f"GPU Memory: {allocated:.2f} GB allocated, {reserved:.2f} GB reserved")
    else:
        ram = psutil.Process().memory_info().rss / (1024**3)
        print(f"System RAM: {ram:.2f} GB")

def evaluate_model(model, tokenizer, name):
    print(f"\n{'='*50}\nEvaluating Model: {name}\n{'='*50}")
    print_memory_usage()
    
    total_tokens = 0
    total_time = 0.0

    for i, prompt in enumerate(PROMPTS, 1):
        print(f"\n[Prompt {i}] {prompt}")
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        start_time = time.time()
        # Generate with fixed max tokens to measure throughput
        outputs = model.generate(**inputs, max_new_tokens=50, do_sample=False)
        end_time = time.time()
        
        generation_time = end_time - start_time
        # Count only newly generated tokens
        generated_tokens = len(outputs[0]) - len(inputs.input_ids[0])
        
        total_time += generation_time
        total_tokens += generated_tokens
        
        response = tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)
        print(f"Response: {response.strip()}")
        print(f"Speed: {generated_tokens / generation_time:.2f} tokens/sec")

    avg_throughput = total_tokens / total_time
    print(f"\n--- {name} Summary ---")
    print(f"Average Throughput: {avg_throughput:.2f} tokens/sec")
    print_memory_usage()


def run_experiment():
    print("Loading Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    # 1. Full Precision (bfloat16)
    print("\nLoading Full Precision Model (bf16)...")
    model_bf16 = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, 
        torch_dtype=torch.bfloat16, 
        device_map="auto"
    )
    evaluate_model(model_bf16, tokenizer, "Qwen2.5-1.5B (bf16)")
    
    # Free memory
    del model_bf16
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # 2. Quantized (4-bit bitsandbytes)
    print("\nLoading Quantized Model (4-bit NF4)...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    model_4bit = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, 
        quantization_config=bnb_config, 
        device_map="auto"
    )
    evaluate_model(model_4bit, tokenizer, "Qwen2.5-1.5B (4-bit NF4)")


if __name__ == "__main__":
    try:
        run_experiment()
    except Exception as e:
        print(f"Error during execution: {e}")
        print("Note: If running on a Mac without CUDA, bitsandbytes 4-bit quantization might not be fully supported out-of-the-box.")
        print("For Mac (Apple Silicon), using 'mlx-lm' or 'llama.cpp' (GGUF) is the recommended approach for quantization.")
