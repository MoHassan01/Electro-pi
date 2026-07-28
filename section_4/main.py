import asyncio
import torch
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

# Using a very small model by default so it fits in most test environments
MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

app = FastAPI(title="LLM Inference API")

# Global variables for model and tokenizer
model = None
tokenizer = None

@app.on_event("startup")
def load_model():
    global model, tokenizer
    print(f"Loading model {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto" if torch.cuda.is_available() else "cpu",
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
    )
    print("Model loaded successfully.")


class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 100


@app.post("/generate")
async def generate_stream(request: GenerateRequest):
    """
    Streaming endpoint that returns tokens one by one.
    """
    inputs = tokenizer([request.prompt], return_tensors="pt").to(model.device)
    
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    
    generation_kwargs = dict(
        inputs,
        streamer=streamer,
        max_new_tokens=request.max_tokens,
        do_sample=True,
        top_p=0.9,
        temperature=0.7
    )
    
    # We must run generation in a background thread so it doesn't block the async event loop
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    
    async def token_generator():
        for new_text in streamer:
            # Yield each token to the client as soon as it's generated
            yield new_text
            # Yield control back to the event loop
            await asyncio.sleep(0.01)

    return StreamingResponse(token_generator(), media_type="text/plain")

@app.get("/health")
def health_check():
    return {"status": "ok", "model": MODEL_ID}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
