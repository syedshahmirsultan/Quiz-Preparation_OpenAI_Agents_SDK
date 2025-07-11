from agents import Runner,Agent,OpenAIChatCompletionsModel,RunContextWrapper
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from dataclasses import dataclass


@dataclass
class UserContext:
    name:str
    age:int
    email:str


load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"
client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=openrouter_api_key
)

model = OpenAIChatCompletionsModel(openai_client=client,model=MODEL)

#The parameters are context and agent name and their nam ecan be change but position cannot be changed
def dynamic_instructions(ctx: RunContextWrapper[UserContext], agent:Agent[UserContext]) -> str:
    print("Context:", ctx.context)
    print("Agent Name:", agent.name)
    return f"You are an expert Motivational Speaker and Sells Expert . You always call the user by his name {ctx.context.name} and give them example according to their age {ctx.context.age} and email {ctx.context.email}."
    
    

historian_Agent = Agent[UserContext](
    name="Dekho Suno Samjho Agent",
    instructions=dynamic_instructions,
    model=model)

user_context = UserContext(
"Shahmir",
18,
"syedshahmirsultan@gmail.com")

def main():
    # Passing context in Runner
    result = Runner.run_sync(historian_Agent, "Teach How To sell and also give me motivation",context=user_context)
    return result.final_output