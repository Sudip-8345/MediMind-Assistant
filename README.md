# MediMind-Assistant
### An AI-powered wellness assistant that helps classify user intent (symptom check, lifestyle, medication, or diet query) and generate personalized, evidence-based wellness plans.
### It combines NLP (spaCy + scispaCy), a DistilBERT intent classifier, and LLM-based reasoning (LangChain + GPT model) to provide insights, precautions, and lifestyle recommendations.
***
## Project Pathway
<img width="3296" height="2545" alt="Medical NLP and Personalized Plan Generation" src="https://github.com/user-attachments/assets/f92c7f73-714e-4925-a55a-04d28b17380c" />

***
## Tech Stack

- Python
- LangChain, langchain-Openai (GPT-OSS 120B)
- Transformers (Hugging Face)
- PyTorch
- Spacy, SciSpacy (en_core_sci_md)
- Streamlit
- Scikit-learn
- Pandas / NumPy
***
## Setup & Usage
### 1️⃣ Install dependencies
- git clone https://github.com/Sudip-8345/MediMind-Assistant.git
- cd MediMind-Assistant
- pip install -r requirements.txt

### 2️⃣ Run prediction script
- python MyAssistant.py (local app by vanilla model)
- python AI_assistant.py (local app by LLM)
- streamlit run VanillaApp.py (st app by vanilla model)
- streamlit run AI-app.py (st app by LLM)
- Streamlit run WellnessChatbot.py
***
## App Demo

![myapp2](https://github.com/user-attachments/assets/1b7b94ac-0727-45aa-ab99-1d0dc7e1d658)
![IMG-20250831-WA0050 1](https://github.com/user-attachments/assets/15513612-d777-43fa-a273-ab7eb0e9d51b)

![myapp3](https://github.com/user-attachments/assets/8ec7ed27-7403-4e96-ad4b-882cd1911eea)

***
## Chatbot Demo
![chatbot](https://github.com/user-attachments/assets/0ff0a956-4cf6-43ea-83d8-09f468fbf6a1)

