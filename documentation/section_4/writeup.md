# Section 4: Model Deployment Write-up

### Question: 
*How would this change if you needed to serve 50 concurrent users in production — what would you add (batching, autoscaling, caching, queueing)?*

### Answer:
Serving 50 concurrent users introduces significant memory and computational bottlenecks (specifically KV cache exhaustion). To transition from a local API to a true production-grade endpoint, I would completely pivot the architecture to use **vLLM** deployed on a Kubernetes cluster with NVIDIA GPUs, adding the following components:

1. **vLLM with PagedAttention (Dynamic Batching)**
   The core innovation needed for 50 concurrent users is **PagedAttention**. Traditional inference engines allocate one long, contiguous memory block for a user's KV cache, causing massive memory fragmentation. `vLLM` breaks the cache into fixed-size GPU blocks and manages them using a virtual page table. This allows the attention kernel to jump to non-adjacent pages dynamically, packing thousands of requests densely into GPU memory. This enables **continuous batching**, allowing the model to decode multiple users' tokens in parallel without OOM errors.
   
2. **Queueing (API Gateway & Request Buffer)**
   To handle unpredictable traffic spikes, I would place the inference server behind an API Gateway (like Kong) and a message queue or buffer (like Redis or Kafka). If concurrent requests exceed the GPU's maximum batched sequence length, the queue holds the requests, returning a "processing" status to the client instead of dropping the connection or overwhelming the vLLM scheduler.

3. **Autoscaling (KEDA)**
   In Kubernetes, I would implement **KEDA (Kubernetes Event-driven Autoscaling)**. Instead of scaling based on raw CPU/GPU utilization (which is always 100% during inference), KEDA scales the number of vLLM Pods based on the *length of the incoming queue*. If the queue hits a threshold (e.g., >10 queued requests per replica), a new GPU pod spins up.

4. **Semantic Caching (Redis/GPTCache)**
   If users frequently ask identical or semantically similar questions (e.g., "What are your business hours?"), routing them to the GPU is a waste of compute. I would inject a semantic caching layer (like `GPTCache`) before the inference server. It embeds the incoming query and checks a Vector DB for close matches. If a cache hit occurs, it returns the generated response instantly, completely bypassing the LLM queue and saving immense VRAM.
