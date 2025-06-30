from agents import Agent,Runner,OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from dataclasses import dataclass

@dataclass
class Context:
    customer_name:str
    customer_age:int
    customer_email:str


load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)


sales_Agent = Agent(name="Shahmir Agent",instructions=f"You are an expert Sales Person.",model= model)

context = Context(customer_name="Shahmir",customer_age=20,customer_email="shahmir@gmail.com")

def main():
    result = Runner.run_sync(sales_Agent,"Who is the best sales men in the world !",context=context)
    print(result)
    return result.final_output