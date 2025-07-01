from agents import OpenAIChatCompletionsModel,Agent,Runner, function_tool
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


@function_tool
def add(a,b):
    """Add two numbers"""
    return a+b

@function_tool
def multiply(a,b):
    """Multiply two numbers"""
    return a*b

@function_tool
def divide(a,b):
    """Divide two numbers"""
    return a/b


agent = Agent(name="Shahmir Agent",
instructions="You are an expert manager .Who delegates task to relevant people to get the job done.",
model=model,
tools =[add,multiply,divide])

async def main():
    result = Runner.run_streamed(agent,"Multiply 2 and 3 then add 4 and divide the total with 2 .")
    async for event in result.stream_events():
        # if (events.type == "raw_response_event" and events.data.type == "response.output_text.delta"):
        #     print(events.data.delta)
        if event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("Tool was called !")



def run_main():
    return asyncio.run(main())