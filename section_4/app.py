import os
import sys
from huggingface_hub import hf_hub_download

def main():
    print("Downloading/Locating model from HuggingFace Hub...")
    # Downloads (or finds cached) Qwen 0.5B Q4 GGUF
    model_path = hf_hub_download(
        repo_id="Qwen/Qwen2.5-0.5B-Instruct-GGUF", 
        filename="qwen2.5-0.5b-instruct-q4_k_m.gguf"
    )
    print(f"Model located at: {model_path}")
    print("Starting official llama_cpp.server...")
    
    # We replace the current python process with the llama_cpp.server
    # passing the absolute path to the downloaded model.
    os.execvp(
        sys.executable,
        [
            sys.executable, 
            "-m", "llama_cpp.server", 
            "--model", model_path, 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--n_threads", str(max(1, os.cpu_count() - 1))
        ]
    )

if __name__ == "__main__":
    main()
