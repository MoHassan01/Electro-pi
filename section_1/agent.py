import asyncio
import logging
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    RunContext,
    cli,
)
from livekit.agents.llm import function_tool
from livekit.plugins import deepgram, google

load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("voice-agent")

class DeliveryAssistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a helpful customer support assistant for a food delivery app. "
                "Your interface with users will be voice. "
                "You should be polite, concise, and helpful. "
                "You have access to a tool to check order statuses. "
                "If a user asks about their order, ask for their order ID if they haven't provided it, "
                "then use the get_order_status tool."
            ),
        )

    async def on_enter(self) -> None:
        self.session.generate_reply(instructions="Say exactly: Hi there! Welcome to Foodies Delivery Support. How can I help you today?")

    @function_tool(description="Get the status of a food delivery order")
    async def get_order_status(self, context: RunContext, order_id: str) -> str:
        """
        Look up the order status for a given order ID.
        """
        logger.info(f"LLM invoked get_order_status for order_id: {order_id}")
        mock_database = {
            "123": "Your order is currently being prepared in the kitchen.",
            "456": "Your driver is on the way and is 5 minutes away.",
            "789": "Your order has been delivered."
        }
        
        status = mock_database.get(order_id)
        if status:
            return f"Order {order_id} status: {status}"
        return f"Sorry, I couldn't find an order with ID {order_id}."

server = AgentServer()

@server.rtc_session()
async def entrypoint(ctx: JobContext) -> None:
    logger.info(f"connecting to room {ctx.room.name}")
    
    session = AgentSession(
        stt=deepgram.STT(),       
        llm=google.LLM(),         
        tts=deepgram.TTS(),       
    )

    await session.start(
        agent=DeliveryAssistant(),
        room=ctx.room,
    )

if __name__ == "__main__":
    cli.run_app(server)
