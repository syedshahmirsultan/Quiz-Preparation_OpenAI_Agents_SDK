from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
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
def get_weather(city: str) -> str:
    """
    Gives weather for cities.
    """
    return f"The weather in {city} is sunny with a temperature of 25°C."
@function_tool
def get_quote(topic: str) -> str:                           
    """
    Gives quote for topics.
    """
    return f"Here is a motivational quote about {topic}: 'The only way to do great work is to love what you do.'"
# If you add tools in the cloned agent ,it will have no effect on the original agent
english_agent = Agent(
    name="English Agent",
    instructions="You are an expert English Teacher and tool caller. You are able to answer questions about English and Grammar under 2 lines.",
    model=model,
    tools=[get_weather, get_quote],
)
async def main():
    result = Runner.run_streamed(english_agent, "Give me a quote about learning and also tell me the weather in Karachi", max_turns=2)
    async for event in result.stream_events():
         if (event.type == "raw_response_event" and  isinstance(event.data,ResponseTextDeltaEvent)):
             print(f"Streaming Response: {event.data.delta}")
                
def run():
    return asyncio.run(main())