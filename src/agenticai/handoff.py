from agents import Agent,Runner,OpenAIChatCompletionsModel,handoff,function_tool
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)


science_agent = Agent(
    model=model,
    handoff_description="You have expert level knowledge of Science and can answer any question about Science.",
    instructions="You have expert level knowledge of Science and can answer any question about Science.",
    name="Science Agent"
)


math_agent = Agent(
    model=model,
    handoff_description="You have expert level knowledge of Math and can answer any question about Math.",
    instructions="You have expert level knowledge of Math and can answer any question about Math.",
    name="Math Agent"
)


manager_Agent = Agent(
    model=model,
    instructions="You are a manager agent responsible for delegating tasks only. ",
    name="Manager Agent",
    handoffs =[science_agent,math_agent]
)


def main():
    # result = Runner.run_sync(manager_Agent, "What is Electromagnetism?")
    result = Runner.run_sync(manager_Agent, "What is Linear Alegbra?")
    print(f"Agent Name : {result.last_agent.name}")