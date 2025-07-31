from livekit import agents
from livekit.agents import JobContext, WorkerOptions
from livekit.agents import Agent, AgentSession, AutoSubscribe
from livekit.plugins import openai, silero
from dotenv import load_dotenv
import os

load_dotenv()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    session = AgentSession(
        llm=openai.RealtimeModel(api_key=os.getenv("OPENAI_API_KEY")),
        stt=silero.VAD.load(),
        tts=silero.TTS(),
    )

    agent = Agent(instructions="You are a helpful AI voice assistant.")
    await session.start(room=ctx.room, agent=agent)

if __name__ == "__main__":
    agents.cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint)
    )
