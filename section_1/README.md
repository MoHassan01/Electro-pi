# Section 1: LiveKit Agents

This section contains a minimal voice assistant (built with LiveKit's new v1.6 AgentServer architecture) that connects to a room and provides food delivery support using a tool call (`get_order_status`).

## Prerequisites & API Keys
You will need three sets of free API keys for this section:
1. **Google (Gemini) API Key** (for the LLM): Get it from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. **Deepgram API Key** (for STT and TTS): Get it from the [Deepgram Console](https://console.deepgram.com/).
3. **LiveKit Cloud Keys**: Sign in to [LiveKit Cloud](https://cloud.livekit.io/), create a project, and go to **Project Settings -> Keys** to get your URL, API Key, and API Secret.

## Setup and Execution
1. Navigate into the `section_1` directory (if not already there):
   ```bash
   cd section_1
   ```

2. Install the necessary dependencies:
   ```bash
   pip install livekit-agents livekit-plugins-google livekit-plugins-deepgram livekit-plugins-silero python-dotenv
   ```

3. Create a file named `.env.local` inside the `section_1` directory, and paste in your keys:
   ```env
   GOOGLE_API_KEY="your-google-api-key"
   DEEPGRAM_API_KEY="your-deepgram-api-key"
   LIVEKIT_URL="wss://your-project.livekit.cloud"
   LIVEKIT_API_KEY="your-livekit-api-key"
   LIVEKIT_API_SECRET="your-livekit-api-secret"
   ```

4. Start the agent:
   ```bash
   python agent.py start
   ```
   *(To stop the agent cleanly, press `Ctrl+C` in your terminal)*

## How to Test
Once the agent says "registered worker" in your terminal, navigate to the **Sandbox** in your LiveKit Cloud dashboard. Connect to the room and start speaking. Try asking: *"Can you check the status of my order? The ID is 456."*

*See `../documentation/section_1/writeup.md` for thoughts on barge-in and tool safety, and `../documentation/section_1/handover.md` for steps taken.*
