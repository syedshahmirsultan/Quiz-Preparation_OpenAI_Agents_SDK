from agents import (
    Agent,Runner,OpenAIChatCompletionsModel,handoff,function_tool,
     input_guardrail, output_guardrail,GuardrailFunctionOutput,
     InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered,RunContextWrapper)

from dataclasses import dataclass
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI


@dataclass
class UserContext:
    name: str
    age: int
    email: str

@dataclass
class OutputStructure:
    reason:str



@dataclass
class GuardrailType:
    is_math:bool
    reason:str

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)



scientific_agent = Agent(name="Scientific Agent",instructions="You give the authentic AI History.", handoff_description="You provide authentic and precise information about the History of AI.",model=model)

@function_tool
def motivation_agent(context:RunContextWrapper):
    return f"Nice Job mate {context.context.name}"

def on_handoff(context:RunContextWrapper    ):
    return f"Thank God you are {context.context.name}. You have called the {agent.name}."



guardrail_agent = Agent(name="Guardrail Agent",instructions="You check if the question is about maths or not.",model=model,
output_type=GuardrailType)

@input_guardrail
async def math_guardrail(context:RunContextWrapper,agent:Agent,input:str):
    result = await Runner.run(guardrail_agent,input=input,context=context)
    print(f"I got you {context.context.name}")
    return GuardrailFunctionOutput(output_info=result.final_output,tripwire_triggered= result.final_output.is_math)
    




# history_agent = Agent(name="History Agent",instructions="You are an expert in History.",model=model, handoffs=handoff(agent=scientific_agent,on_handoff=on_handoff,tool_name_override="scientific_history_agent", tool_description_override="You provide authentic and precise information about Technology and science History."  )
# ,tools=[motivation_agent],
# output_type=OutputStructure,
# input_guardrails=[math_guardrail])

history_agent = Agent(name="History Agent",instructions="You are an expert in History.",model=model
# ,tools=[motivation_agent],
,output_type=OutputStructure,
input_guardrails=[math_guardrail],
handoffs=[scientific_agent]
)


user_context = UserContext(name="Shahmir",age= 18,email="shahmir@gmail.com")
def main():
    try:
     result = Runner.run_sync(history_agent,"Tell me bout the history of AI",context=user_context)
     print(result.final_output)
    except InputGuardrailTripwireTriggered:
     print("Input Guardrail Triggered")