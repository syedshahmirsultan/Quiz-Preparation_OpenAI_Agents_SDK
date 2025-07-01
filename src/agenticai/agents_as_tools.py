from agents import Agent,Runner,OpenAIChatCompletionsModel
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

spanish_agent = Agent(name="Spanish Agent",instructions="You are an expert an expert translator in Spanish.",model=model)
chinese_agent = Agent(name="Chinese Agent",instructions="You are an expert an expert translator in Chinese.",model=model)


agent = Agent(name="Translator Agent",instructions=["You are an expert translator in Spanish and Chinese.","You can translate text from English to Spanish and Chinese.","You can also translate text from Spanish and Chinese to English."],
model=model,
tools=[spanish_agent.as_tool(tool_name="translate_to_spanish",tool_description="You are an expert in translating text from English to Spanish.")
,chinese_agent.as_tool(tool_name="translate_to_chinese",tool_description="You are an expert in translating text from English to Chinese.")
])

# Tool_Name and Agent Name can never be same .If ever same it gives 400 error.
def main():
    result = Runner.run_sync(agent,"Translate this text 'Hello My name is Syed Shahmir Sultan' from English to Spanish and Chinese.")
    print(result.final_output)

