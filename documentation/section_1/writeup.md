# Section 1 Write-up: LiveKit Agents

## 1. Supporting Barge-in / Interruption Handling
Barge-in allows the user to interrupt the agent while it is speaking, creating a natural back-and-forth conversation. In the LiveKit Agents SDK, `VoicePipelineAgent` already has robust underlying support for barge-in, but to properly handle it in a production scenario, I would extend our implementation as follows:

- **Configure VAD (Voice Activity Detection)**: The agent relies on VAD (e.g., `silero.VAD`) to know when the user starts speaking. I would fine-tune the VAD parameters (like `min_speech_duration` and `min_silence_duration`) so that minor background noises don't falsely interrupt the agent, but actual human speech halts the TTS immediately.
- **Enable Interruption in TTS**: I would ensure `allow_interruptions=True` is passed to all `agent.say()` calls.
- **State Management**: If the agent is interrupted while reading a long string of data (e.g., a complex order summary), the LLM needs to know it was interrupted so it doesn't lose context. LiveKit handles injecting the partial transcript (what was actually synthesized and spoken before interruption) back into the chat context. 
- **Graceful Resumption**: I would add a prompt directive (system persona) telling the LLM to gracefully acknowledge interruptions. For instance, if the user interrupts with "Wait, no, it was order 123", the LLM should seamlessly pivot without finishing the previous thought.

## 2. Adding a Second Tool Safely
To add a second tool safely (e.g., `cancel_order`), I would take the following precautions regarding schema and error handling:

- **Strict Type Hinting and Docstrings**: The `@llm.ai_callable` decorator infers the schema from Python type hints and docstrings. I would ensure the docstring clearly explains *when* the LLM should use the tool and explicitly describe every parameter (e.g., `def cancel_order(self, order_id: str, reason: str) -> str:`).
- **Graceful Error Handling**: Network or DB calls can fail. Instead of raising an uncaught exception which might crash the agent or cause silent failures, I would wrap the tool logic in a `try...except` block. 
  - If a failure occurs, the tool should return a string like `"Error: Database timeout. Please ask the user to wait a moment and try again."` This feeds the error back to the LLM as text, allowing the LLM to naturally apologize to the user and handle the failure conversationally.
- **Validation**: Inside the tool, I would validate the inputs (e.g., ensuring `order_id` matches a regex) before hitting the backend. If validation fails, return an informative error string back to the LLM.
- **Timeouts**: Since tool calls block the conversational flow, I would enforce strict asynchronous timeouts (`asyncio.wait_for`) on the backend API call within the tool to prevent the voice agent from staying silent for too long if the backend hangs.
