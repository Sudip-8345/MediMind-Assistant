import pandas as pd
from collections import defaultdict

def load_symptom_condition_mapping(data_path='data/dataset.csv'):
    df_symptoms = pd.read_csv(data_path)
    symptom_cond_dict_map = defaultdict(list)
    for _, row in df_symptoms.iterrows():
        disease = row['Disease']
        for col in df_symptoms.columns[1:]:
            symptom = row[col]
            if pd.notna(symptom):
                symptom_cond_dict_map[symptom.lower()].append(disease)
    return symptom_cond_dict_map