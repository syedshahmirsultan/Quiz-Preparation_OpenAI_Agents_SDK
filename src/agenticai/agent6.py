from agents import Agent,Runner,OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
from pydantic import BaseModel

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"


class OutputStructure(BaseModel):
    inventor:str
    year:int
    month:str
    invention:str
    historical_event:str
    significance:str


client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)


agent = Agent(name="Shahmir Agent",
instructions="You are an Expert AI Historian, Who knows the history of AI evolution from the start .Always tell the history in precise manner.",
model=model,
output_type=OutputStructure)

def main():
  result = Runner.run_sync(agent,"who invented the Neural Networks ?")
#   return result.final_output.inventor
  return result.final_output.dict()

