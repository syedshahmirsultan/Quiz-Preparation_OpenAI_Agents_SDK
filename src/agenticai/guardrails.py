from agents import Agent,Runner,OpenAIChatCompletionsModel,function_tool,RunContextWrapper,GuardrailFunctionOutput,InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered,input_guardrail,output_guardrail
from openai import AsyncOpenAI  
from dotenv import load_dotenv
import os
import asyncio
from pydantic import BaseModel

load_dotenv()


class GuardrailClass(BaseModel):
    is_dates:bool
    reason:str


class OutputClass(BaseModel):
    response:str

class UserContext(BaseModel):
    name:str
    age:int
    email:str

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)


guardrail_agent = Agent(name="Guardrail Agent", instructions= "You have to check if response contains anykind of dates",model=model,output_type=GuardrailClass)


@output_guardrail
async def guardrail_check(context:RunContextWrapper,agent:Agent,output:OutputClass):
    result = await Runner.run(guardrail_agent,output.response,context=context)
    print(f"I got you {context.context.name}")
    return GuardrailFunctionOutput(output_info=result.final_output,tripwire_triggered= result.final_output.is_dates)
    

historian_agent = Agent(name="Historian Agent",instructions="You are an expert in History.",model=model,output_guardrails=[guardrail_check],output_type=OutputClass)



async def main():
    try :
        result = await Runner.run(historian_agent,"hi",context=UserContext(name="Shahmir",age=18,email="shahmir@gmail.com"))
        print(result.final_output)
    except OutputGuardrailTripwireTriggered:
        print("Output Guardrail Triggered")


def run():
    asyncio.run(main())
