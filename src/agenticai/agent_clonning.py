from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os   
# Load environment variables from .env file
load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"

MODEL = "google/gemini-2.0-flash-001"
client = AsyncOpenAI(                   
    base_url=BASE_URL,
    api_key=openrouter_api_key
)   
model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)

@function_tool
def get_weather(city:str)-> str:
    """
    Gives weather for cities.
    """
    return f"The weather in {city} is sunny with a temperature of 25°C."

math_agent = Agent(
    name="Math Agent",
    instructions="You are an expert Mathematician and Physicist. You are able to answer questions about math and physics under 2 lines.",
    model=model
)

# If you add tools in the cloned agent ,it will have no effect on the original agent
english_agent = math_agent.clone(
    name="English Agent",
    instructions="You are an expert English Teacher and tool caller. You are able to answer questions about English and Grammar under 2 lines.",
    tools =[get_weather]
)

def main():
    result = Runner.run_sync(math_agent, "What is the weather in Karachi ?")
    print(f"Math Agent Response: {result.final_output}")

    result = Runner.run_sync(english_agent, "What is the weather in Karachi ?")
    print(f"English Agent Response: {result.final_output}")
