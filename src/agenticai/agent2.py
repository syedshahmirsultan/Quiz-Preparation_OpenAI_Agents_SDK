from agents import OpenAIChatCompletionsModel,Runner,Agent, function_tool
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

def dynamic_instructions():
 instructions = "You are an expert Historian and Philosopher. You are able to answer questions about history and philosophy under 2 lines ."
 return instructions


agent = Agent(
    name="Shahmir Agent",
    model=model,
    instructions=dynamic_instructions())

def main():
    result = Runner.run_sync(agent,"Who are you ?")
    return result.final_output

@function_tool
def get_current_date(x:int):
    """Multiply the number by 2"""
    return x *2



historian_agent = Agent(
    name="Historian Agent",
    model=model,
    instructions="  If there is any multiply related question Call the tool get_current_date.",
    tools=[get_current_date],
    )


def history_run():
    result = Runner.run_sync(historian_agent,"Multiply 5 by 2")
    return result.final_output