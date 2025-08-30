import streamlit as st
import pandas as pd
import torch
import spacy
import json

from LoadFiles.load_model import load_distilbert_model
from sklearn.preprocessing import LabelEncoder
from LoadFiles.load_spacy import get_medical_nlp_model, extract_symptoms
from LoadFiles.wellness_utils import detect_intent, generate_precautions, format_wellness_plan
from LoadFiles.load_data import load_symptom_condition_mapping
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="AI Wellness Assistant", page_icon="🩺")
st.title('🩺 AI Wellness Assistant')
st.write('Your personal health and wellness guide powered by NLP')

status_placeholder = st.empty()
status_placeholder.info("⏳ Loading models, please wait...")

# Load models and data 
model, tokenizer = load_distilbert_model()

# Load intent dataset
with open('intent_dataset.json', mode='rb') as file:
    intents = json.load(file)
data = []
for label, examples in intents.items():
    for ex in examples:
        data.append((ex, label))
# Create DataFrame and Label Encoder
df = pd.DataFrame(data, columns=["text", "label"])
le = LabelEncoder()
df['label_id'] = le.fit_transform(df.label)

# Build symptom
data_path = 'data/dataset.csv'
symptom_cond_dict_map = load_symptom_condition_mapping(data_path)

# Load Precautions
precautions_df = pd.read_csv('data/symptom_precaution.csv')
recommendations = {}
for _, row in precautions_df.iterrows():
    disease = row['Disease'].strip().lower().replace("-", " ").replace("_", " ")
    precautions = [str(row[col]).strip() for col in precautions_df.columns[1:]]
    recommendations[disease] = precautions

# Load Spacy model
nlp = get_medical_nlp_model()

status_placeholder.success(" Models loaded successfully.")

def wellness_assistant(user_text):
    intent = detect_intent(user_text, tokenizer, model, label_encoder=le)
    symptoms = extract_symptoms(user_text) if intent == 'symptom_check' else []
    plan = generate_precautions(symptoms, symptom_cond_dict_map, recommendations) if symptoms else {}
    return intent, symptoms, plan

user_input = st.text_area('Enter your health concern: ')

if st.button("Analyze"):
    if user_input.strip():
        with st.spinner("Analyzing your concern..."):
            intent, symptoms, plan = wellness_assistant(user_input)

        st.subheader("🔍 Detected Intent:")
        st.write(intent)

        if symptoms:
            st.subheader("🩺 Extracted Symptoms:")
            st.write(", ".join(symptoms))

        if plan:
            st.subheader("📋 Personalized Wellness Plan:")
            st.write(format_wellness_plan(symptoms, plan))
        else:
            st.warning("No specific recommendations found.")
    else:
        st.warning("Please enter a concern first.")

st.markdown("---")
st.caption("⚠️ This is not medical diagnosis. Please consult a healthcare professional for any medical concerns.")