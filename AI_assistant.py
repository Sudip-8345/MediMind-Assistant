from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = ChatOpenAI(
    openai_api_base="https://router.huggingface.co/v1",
    model="openai/gpt-oss-120b:cerebras",
    temperature=0.3,
    openai_api_key=os.getenv("HF_TOKEN")
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are an evidence-based medical assistant. 
     First, classify the user's intent as either 'Symptom Check' or 'Lifestyle Query' or 'Medication Query','Diet Query' and show it.
     Generate a personalized wellness plan symptom case only in consize JSON format with: 
     condition_summary, precautions, yoga_plan, diet_plan, medication_advice. 
     Prioritize natural care and preventive care unless the condition is critical, otherwise
     If the intent is 'Lifestyle Query', 'Medication Query' or 'Diet Query ', provide relevant advice in JSON format with keys: intent, advice."""),
    ("human", "User symptoms: {user_text}")
])

def generate_wellness_plan(user_text):
    messages = prompt_template.format_messages(user_text=user_text)
    response = llm.invoke(messages)
    
    try:
        return json.loads(response.content)
    except:
        return response.content 

if __name__ == "__main__":
    user_text = input("Tell me your intents: ")
    plan = generate_wellness_plan(user_text)
    print("Personalized Wellness Plan:")
    print(json.dumps(plan, indent=2))