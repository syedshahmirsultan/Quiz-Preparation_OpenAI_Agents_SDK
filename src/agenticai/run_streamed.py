from agents import OpenAIChatCompletionsModel,Agent,Runner
from openai import AsyncOpenAI
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
import os
load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)

agent = Agent(name="Shahmir Agent",
instructions="You are an Expert AI Historian, Who knows the history of AI evolution from the start .Always tell the history in precise manner.",
model=model)

async def main():
    result = Runner.run_streamed(agent,"When was the first Programming Language was introduced ?",)
    async for event in result.stream_events():
        # if (events.type == "raw_response_event" and events.data.type == "response.output_text.delta"):
        #     print(events.data.delta)
        if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
            print(event.data.delta)


def run_main():
    return asyncio.run(main())