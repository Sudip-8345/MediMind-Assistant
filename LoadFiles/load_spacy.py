import spacy
import scispacy
from scispacy.linking import EntityLinker
import os


def get_medical_nlp_model(model_path="en_ner_bc5cdr_md", use_linker=True):
    
    if os.path.exists(model_path):
        print(f"Loading cached medical NLP model from {model_path} ...")
        return spacy.load(model_path)

    print("Loading fresh medical NLP model (this may take a while)...")
    nlp = spacy.load(model_path)

    if use_linker:
        nlp.add_pipe("scispacy_linker", config={
            "resolve_abbreviations": True,
            "linker_name": "umls"
        })

    nlp.to_disk(model_path)
    print(f"Medical NLP model saved to {model_path}")

    return nlp


def extract_umls_diseases(text, nlp):
    doc = nlp(text)
    diseases = []
    
    # Check if linker is available
    if "scispacy_linker" in nlp.pipe_names:
        linker = nlp.get_pipe("scispacy_linker")
        for ent in doc.ents:
            if hasattr(ent._, 'kb_ents') and ent._.kb_ents:
                for cui, score in ent._.kb_ents:
                    if cui in linker.kb.cui_to_entity:
                        umls_ent = linker.kb.cui_to_entity[cui]
                        diseases.append(umls_ent.canonical_name)
                        break
    else:
        for ent in doc.ents:
            diseases.append(ent.text)
    
    return diseases




if __name__ == "__main__":
    sample_text = "I have a skin rash and diabetes."
    results = extract_umls_diseases(sample_text, nlp=get_medical_nlp_model())

    print("\n Extracted Entities:")
    for res in results:
        print(res)
