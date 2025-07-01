from agents import Agent,Runner,OpenAIChatCompletionsModel,run_demo_loop
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)



async def main():
    agent = Agent(name="Shahmir Agent",instructions="You are an Expert AI Historian, Who knows the history of AI evolution from the start .Always tell the history in precise manner.",model=model)
    return await run_demo_loop(agent)


def run_main():
    return asyncio.run(main())
