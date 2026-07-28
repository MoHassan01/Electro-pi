import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "http://localhost:8000/v1/chat/completions"
CONCURRENT_REQUESTS = 10
PROMPT = "Write a 50-word story about a robot learning to paint."

def make_request(request_id):
    start_time = time.time()
    first_token_time = None
    
    payload = {
        "messages": [{"role": "user", "content": PROMPT}],
        "max_tokens": 50,
        "temperature": 0.7,
        "stream": True
    }
    
    try:
        # Use stream=True in requests
        response = requests.post(API_URL, json=payload, stream=True, timeout=60)
        
        if response.status_code != 200:
            print(f"[Req {request_id}] Failed with status: {response.status_code}")
            return None
            
        full_response = ""
        # Iterate over Server-Sent Events
        for line in response.iter_lines():
            if line:
                if not first_token_time:
                    first_token_time = time.time()
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    data_str = decoded_line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        content = data['choices'][0]['delta'].get('content', '')
                        full_response += content
                    except:
                        pass
                        
        end_time = time.time()
        
        ttft = first_token_time - start_time if first_token_time else 0
        total_latency = end_time - start_time
        
        print(f"[Req {request_id}] TTFT: {ttft:.3f}s | Total Latency: {total_latency:.3f}s")
        return {
            "ttft": ttft,
            "total_latency": total_latency
        }
    except Exception as e:
        print(f"[Req {request_id}] Error: {e}")
        return None

def main():
    print(f"Starting Load Test with {CONCURRENT_REQUESTS} concurrent requests...")
    print(f"Target URL: {API_URL}")
    print("-" * 50)
    
    start_test_time = time.time()
    
    results = []
    # Fire 10 concurrent requests using a thread pool
    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = [executor.submit(make_request, i+1) for i in range(CONCURRENT_REQUESTS)]
        for future in as_completed(futures):
            results.append(future.result())
            
    end_test_time = time.time()
    
    valid_results = [r for r in results if r is not None]
    
    if not valid_results:
        print("All requests failed. Is the Docker container running?")
        return
        
    avg_ttft = sum(r["ttft"] for r in valid_results) / len(valid_results)
    avg_total = sum(r["total_latency"] for r in valid_results) / len(valid_results)
    
    print("-" * 50)
    print("LOAD TEST RESULTS (10 Concurrent Requests)")
    print("-" * 50)
    print(f"Successful Requests: {len(valid_results)}/{CONCURRENT_REQUESTS}")
    print(f"Average Time-to-First-Token (TTFT): {avg_ttft:.3f} seconds")
    print(f"Average Total Latency:              {avg_total:.3f} seconds")
    print(f"Total Test Wall-Clock Time:         {end_test_time - start_test_time:.3f} seconds")

if __name__ == "__main__":
    main()
