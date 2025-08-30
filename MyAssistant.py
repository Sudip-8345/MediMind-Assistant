import torch
from LoadFiles.load_model import load_distilbert_model
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import json
import spacy
from collections import defaultdict, Counter
from scispacy.linking import EntityLinker
from LoadFiles.load_spacy import get_medical_nlp_model, extract_symptoms
from LoadFiles.wellness_utils import detect_intent, generate_precautions, format_wellness_plan
from LoadFiles.load_data import load_symptom_condition_mapping
import warnings
warnings.filterwarnings("ignore")

# Load models
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

# Build recommendations dictionary
recommendations = {}
for _, row in precautions_df.iterrows():
    disease = row['Disease'].strip().lower().replace("-", " ").replace("_", " ")
    precautions = [str(row[col]).strip() for col in precautions_df.columns[1:]]
    recommendations[disease] = precautions

# Load Spacy model
nlp = get_medical_nlp_model()
model, tokenizer = load_distilbert_model()

def wellness_assistant(user_text):
    intent = detect_intent(user_text, tokenizer, model, label_encoder=le)
    symptoms = extract_symptoms(user_text) if intent == 'symptom_check' else []
    plan = generate_precautions(symptoms,symptom_cond_dict_map,recommendations) if symptoms else {}
    return intent, symptoms, plan

# Test 
user_text = " I am vomiting and have a headache and fever"
intent, symptoms, plan = wellness_assistant(user_text)
print("🔍 Intent:", intent)
print("🩺 Symptoms:", symptoms)
print("\n📋 Wellness Plan:\n", format_wellness_plan(symptoms, plan))