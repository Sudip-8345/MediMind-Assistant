import spacy
import scispacy
from scispacy.linking import EntityLinker
import pickle
import os

def get_medical_nlp_model(model_path="sci_md_300k"):
    
    if os.path.exists(model_path):
        return spacy.load(model_path)
    
    print(" Loading fresh medical NLP model (this may take a while)...")
    nlp = spacy.load("en_core_sci_md")
    # nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
    
    nlp.to_disk(model_path)
    print(f" Medical NLP model saved to {model_path}")
    
    return nlp

def extract_symptoms(user_text):
    special_nlp = get_medical_nlp_model()
    doc = special_nlp(user_text)
    extracted = [ent.text.lower() for ent in doc.ents]
    return extracted

