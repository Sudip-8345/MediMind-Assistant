import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer

def load_distilbert_model(model_path='./sentiment_model'):
    model = DistilBertForSequenceClassification.from_pretrained(model_path)
    tokenizer = DistilBertTokenizer.from_pretrained(model_path)
    model.eval()
    return model, tokenizer