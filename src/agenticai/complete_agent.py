from agents import Agent,Runner,OpenAIChatCompletionsModel,function_tool,RunContextWrapper,input_guardrail,output_guardrail,GuardrailFunctionOutput,InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import asyncio


load_dotenv()

# User Context
class UserContext(BaseModel):
    name:str
    age:int
    email:str

# Input Guardrail Class
class GuardrailClass(BaseModel):
    is_sports:bool
    reason:str

# Output Guardrail Class
class OutputClass(BaseModel):
    response:str
# Output Guardrail Agent Output Class
class OutputGuardrailClass(BaseModel):
    is_number:bool
    reason:str

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-001"

client = AsyncOpenAI(
base_url=BASE_URL,
api_key=openrouter_api_key)

model = OpenAIChatCompletionsModel(openai_client=client, model=MODEL)

# Guardrail Agent
guardrail_agent = Agent(name="Guardrail Agent",instructions="You have to check if the question is related to sports or not .",model=model, output_type=GuardrailClass)

# Output Guardrail Agent
output_guardrail_agent = Agent(name="Output Guardrail Agent",instructions="You have to check if the response contains any number data in the response or not . example(100,50000 or etc) .",model=model, output_type=OutputGuardrailClass)

# Input Guardrail Function
@input_guardrail
async def guardrail_check(context:RunContextWrapper,agent:Agent,input:str):
    result = await Runner.run(guardrail_agent,input,context=context)
    print(f"{context.context.name}, Input Guardrail Function Called !")
    return GuardrailFunctionOutput(output_info=result.final_output,tripwire_triggered= result.final_output.is_sports)

# Output Guardrail Function
@output_guardrail
async def output_guardrail_check(context:RunContextWrapper,agent:Agent,output:OutputClass):
    result = await Runner.run(output_guardrail_agent,output.response,context=context)
    print(f"{context.context.name}, Output Guardrail Function Called !")
    return GuardrailFunctionOutput(output_info=result.final_output,tripwire_triggered= result.final_output.is_number)


# Financial Agent
financial_agent = Agent(name="Financial Agent",instructions="You are an expert Financial Advisor. You are able to answer questions about finance and investment under 2 lines .",model=model,output_type=OutputClass,output_guardrails=[output_guardrail_check])

# Career Agent
career_agent = Agent(name="Career Agent",instructions="You are an expert Career Advisor. You are able to answer questions about career and job under 2 lines .",model=model,output_type=OutputClass,output_guardrails=[output_guardrail_check])

# Parent Agent
parent_agent = Agent(name="Parent Agent",instructions="You are an expert Parent Advisor. You are able to answer questions about parent and child under 2 lines .",model=model,output_type=OutputClass,output_guardrails=[output_guardrail_check])

# Manager Agent
manager_agent = Agent(name="Manager Agent",instructions="You are an expert Manager Agent which delegats tasks to different agents",
model=model,
handoffs=[financial_agent,career_agent,parent_agent],
input_guardrails=[guardrail_check],
output_guardrails=[output_guardrail_check]
)




async def main():
    try: 
        # result = await Runner.run(manager_agent,"What career should I pursue ?",context=UserContext(name="Shahmir",age=18,email="shahmir@gmail.com"))
        # result = await Runner.run(manager_agent,"What do you think If I want to pursue my career in football",context=UserContext(name="Shahmir",age=18,email="shahmir@gmail.com"))
        result = await Runner.run(manager_agent,"If I am a teacher and I have 50 students and they all pay me 10000 rupees a month and I want to retire tell me what should I do with this money and never add numbers in the answers",context=UserContext(name="Shahmir",age=18,email="shahmir@gmail.com"))

        print(f"Manager Agent Response: {result.final_output}")
        print("Last Agent Name",result.last_agent.name)
    except InputGuardrailTripwireTriggered:
        print("Input Guardrail Triggered")
    except OutputGuardrailTripwireTriggered:
        print("Output Guardrail Triggered")


def run():
   return asyncio.run(main())
