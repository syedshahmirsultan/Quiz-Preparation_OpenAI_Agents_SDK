from agents import Agent,Runner,OpenAIChatCompletionsModel,function_tool
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)

@function_tool
def get_weather(city):
    """Get the weather for a city"""
    return f"The weather in {city} is sunny."

@function_tool
def get_temperature(city):
    """Get the temperature for a city"""
    return f"The temperature in {city} is 25 degrees Celsius."

agent = Agent(name="Shahmir Agent",
instructions="You are an expert Media Reporter.",
model=model,
tools = [get_weather,get_temperature])

# def main():
#     for tool in agent.tools:
#         print(tool.name)
#         print(tool.description)
#         print(tool.params_json_schema)


def main():
    result = Runner.run_sync(agent,"What is the weather and temperature in SF?")
    print(result.final_output)