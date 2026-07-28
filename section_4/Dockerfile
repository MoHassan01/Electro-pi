FROM python:3.10-slim

WORKDIR /app

# Install build dependencies for llama-cpp-python C++ compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Pre-download the model into the docker image so it doesn't download on every container start
# We do this by running a tiny python snippet that triggers hf_hub_download
RUN python -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='Qwen/Qwen2.5-0.5B-Instruct-GGUF', filename='qwen2.5-0.5b-instruct-q4_k_m.gguf')"

# Expose API port
EXPOSE 8000

# Run the launcher script
CMD ["python", "app.py"]
