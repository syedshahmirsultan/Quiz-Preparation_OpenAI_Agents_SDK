from openai import AsyncOpenAI
from agents import Agent,Runner,OpenAIChatCompletionsModel
from typing import List
from dotenv import load_dotenv
import os
from pydantic import BaseModel

class StructuredOutput(BaseModel):
    date:str
    duration: str
    events: List[str]
    famous_persons: List[str]
    reason: str
    who_started: str
    who_ended: str
    results: List[str]
    when_happened: str 
    refered_event:str

    
# Load environment variables from .env file
load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(base_url = BASE_URL, api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client,model=MODEL)

historian_Agent = Agent(
    name="Shahmir Agent",
    instructions="You are an expert Historian and Philosopher. You are able to answer questions about history and philosophy .The answers should always be precise under 150 words.",
    model= model,
    # New Argument for structured output
    output_type=StructuredOutput)

def main():
    queries = ["Tell me about the World War 1 briefly ?","Tell me about the World War 2 briefly ?"]
    for query in queries:
        result = Runner.run_sync(historian_Agent,query)
        print(f"Event Details :{result.final_output}")
    
