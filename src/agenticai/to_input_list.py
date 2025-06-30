from agents import Agent,Runner,OpenAIChatCompletionsModel
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

agent = Agent(name="Shahmir Agent",
instructions="You are an Expert AI Historian, Who knows the history of AI evolution from the start .Always tell the history in precise manner.",
model=model)


def main():
  result = Runner.run_sync(agent,"When was the first Programming Language was introduced ?") 
  print("Result :",result.final_output)
  input_for_next = result.to_input_list() + [{"role": "user", "content": "When was Python Programming Language was introduced ?"}]
  print("Input for next :",input_for_next)
  final_result = Runner.run_sync(agent,input_for_next)
#   return result.last_agent.instructions
  return final_result.final_output


