import streamlit as st
import json
from LoadFiles.load_spacy import get_medical_nlp_model, extract_umls_diseases
from langchain.agents import tool, initialize_agent, AgentType
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Load NLP model once (cache)
@st.cache_resource
def load_models():
    special_nlp = get_medical_nlp_model()
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
    return special_nlp, llm

special_nlp, llm = load_models()

# Prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are an evidence-based medical assistant.
     First, classify the user's intent as either 'symptom check', 'lifestyle query', 'medication query', or 'diet query' and show it.
     If symptom check:
       Generate a concise JSON response with:
       condition_summary, precautions, yoga_plan, diet_plan, medication_advice
     If lifestyle/medication/diet query:
       Provide JSON with: intent, advice.
     Always respond ONLY in valid JSON format."""),
    ("human", "User symptoms: {user_text}\nRecognized conditions: {conditions}")
])

@tool
def generate_wellness_plan(user_text: str, conditions: list) -> str:
    """
    Generates a personalized wellness plan based on user symptoms and recognized conditions.
    """
    messages = prompt_template.format_messages(user_text=user_text, conditions=conditions)
    response = llm.invoke(messages)

    try:
        return json.dumps(json.loads(response.content))
    except Exception as e:
        return response.content

agent = initialize_agent(
    tools=[generate_wellness_plan],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

def generate_plan(user_text):
    conditions = extract_umls_diseases(user_text, nlp=special_nlp)
    return agent.invoke({"input": {"user_text": user_text, "conditions": conditions}})

# ----------------- Streamlit UI -----------------
st.title("🩺 AI Medical Wellness Assistant")
st.write("Get evidence-based suggestions for your symptoms, lifestyle, or diet queries.")

user_text = st.text_area("Describe your symptoms or health query:", "")

if st.button("Generate Wellness Plan"):
    if user_text.strip():
        with st.spinner("Analyzing..."):
            plan = generate_plan(user_text)

        st.subheader("Personalized Wellness Plan")
        try:
            output = plan["output"]
            st.write(output)

            # If JSON structure was returned
            if isinstance(output, dict):
                st.json(output)
        except Exception:
            st.write(plan)
    else:
        st.warning("Please enter your symptoms or query.")
