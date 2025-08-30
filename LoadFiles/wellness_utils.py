import torch
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from LoadFiles.load_data import load_symptom_condition_mapping
from LoadFiles.load_model import load_distilbert_model

def detect_intent(user_text, tokenizer, model, label_encoder):
    inputs = tokenizer(user_text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    return label_encoder.inverse_transform([pred])[0]

def generate_precautions(symptoms, symptom_cond_dict_map, recommendations, top_k=3):
    cond_counter = Counter()
    for sym in symptoms:
        variations = [sym, f" {sym}", sym.strip()]
        found = False
        for variation in variations:
            if variation in symptom_cond_dict_map:
                cond_counter.update(symptom_cond_dict_map[variation])
                found = True
                break
        if not found:
            print(f"Symptom '{sym}' not found in dictionary")
    top_conditions = cond_counter.most_common(top_k)
    plans = {}
    for disease, count in top_conditions:
        disease_key = disease.strip().lower().replace("-", " ").replace("_", " ")
        if disease_key in recommendations:
            plans[disease] = {
                'Matched_symptoms': count,
                'Precautions': recommendations[disease_key]
            }
        else:
            plans[disease] = {
                'Matched_symptoms': count,
                'Precautions': ['Consult a doctor or Search in ChatGPT/Google']
            }
    return plans

def format_wellness_plan(symptoms, plan):
    if not plan:
        return "No clear recommendations. Please consult a doctor."

    response = f"Based on your reported symptoms ({', '.join(symptoms)}), here's a wellness plan:\n\n"
    for cond, details in plan.items():
        response += f"*Possible condition:* **{cond}** (matched symptoms: {details['Matched_symptoms']})\n"
        response += f"Recommendations:\n"
        for i, precaution in enumerate(details['Precautions'], 1):
            if precaution.lower() != 'nan':
                response += f"  {i}. {precaution}\n"
        response += "\n"
    response += "This is not a medical diagnosis. Please consult a doctor if symptoms persist."
    return response
