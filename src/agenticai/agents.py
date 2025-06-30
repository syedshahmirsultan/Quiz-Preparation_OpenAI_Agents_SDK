import asyncio
from openai import AsyncOpenAI
from agents import Agent,Runner,OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)


historian_Agent = Agent(name="Shahmir Agent",instructions="You are an expert Historian and Philosopher. You are able to answer questions about history and philosophy under 2 lines .",model= model)

def main():
    result = Runner.run_sync(historian_Agent,"When Pakistn got independence? What was the role of Allama Iqbal in Pakistan's independence?")
    return result.final_output



