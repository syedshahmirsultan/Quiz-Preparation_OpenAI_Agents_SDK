from agents import Agent,Runner,OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
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

org_agent = agent.clone(instructions="You are an expert Pyhton Programmer . Who only returns the Python code without ny explanation or any other text.")

def main():
  result = Runner.run_sync(org_agent,"Write a simple Hello world code")  
#   return result.final_output['inventor']
  return result.final_output