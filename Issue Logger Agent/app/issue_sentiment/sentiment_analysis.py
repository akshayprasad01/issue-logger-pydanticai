import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.special import softmax

class Sentiment:
    @classmethod
    def analyze_sentiment_bert(cls, *, text: str) -> str:
        """
        Performs sentiment analysis using DistilBERT and returns 'Positive', 'Negative', or 'Neutral'.
        """
        # Load pre-trained DistilBERT model and tokenizer for sentiment analysis
        SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
        tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL)
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        
        scores = softmax(outputs.logits.numpy()[0])  # Convert logits to probabilities
        positive_score, negative_score = scores[1], scores[0]  # SST-2 labels: [Negative, Positive]

        if positive_score > 0.6:
            return "Positive"
        elif negative_score > 0.6:
            return "Negative"
        else:
            return "Neutral"