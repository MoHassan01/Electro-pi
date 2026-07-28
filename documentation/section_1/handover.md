# Handover: Section 1 (LiveKit Agents)

## Task Requirements
Build a minimal voice agent with a tool call using the `livekit-agents` Python SDK. The agent should run an STT -> LLM -> TTS pipeline, define a system persona, expose a function tool, and demonstrate the logic. A write-up is also required.

## Steps Taken
1. **Created `agent.py`**:
   - Initialized an `AgentServer` and `AgentSession` architecture (following LiveKit Agents v1.6.7+) using `google` (Gemini) for the LLM, and `deepgram` for STT and TTS to satisfy the pipeline requirement using generous free-tier APIs.
   - Utilized `python-dotenv` to securely load API credentials from a local `.env.local` file.
   - Defined the `DeliveryAssistant` class inheriting from `livekit.agents.Agent`.
   - Exposed the `get_order_status` function directly on the agent using the `@function_tool` decorator to allow the LLM to call it mid-conversation.
   - Configured the system persona by passing `instructions` to the `Agent` superclass defining it as a food delivery support assistant.
   - Implemented a mock database lookup for the tool to simulate a real lookup result.

2. **Created `writeup.md`**:
   - Outlined how to extend the implementation to support barge-in (VAD tuning, `allow_interruptions=True`, and LLM state management).
   - Detailed how to add a second tool safely (strict schema via type hinting, robust `try...except` error handling, returning text errors to the LLM, and asynchronous timeouts).

3. **Isolated Directory**:
   - All files for this section were created inside the `section_1` directory to comply with the project guidelines.

## How to Test
1. Set up a Python virtual environment and install dependencies: `pip install livekit-agents livekit-plugins-google livekit-plugins-deepgram livekit-plugins-silero python-dotenv`.
2. Create a `.env.local` file with your environment variables: `GOOGLE_API_KEY`, `DEEPGRAM_API_KEY`, `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`.
3. Run the agent: `python agent.py start` (press `Ctrl+C` to stop it when finished).
4. Connect to the LiveKit room via a frontend client or LiveKit sandbox to interact via voice and test the tool call.
