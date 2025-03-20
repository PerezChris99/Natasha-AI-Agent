from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime

class AIBrain:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.summarizer = pipeline("summarization")
        self.qa_model = pipeline("question-answering")
        self.chat_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.learned_responses = self._load_learned_data()
        self.conversation_history = []
        
    def _load_learned_data(self):
        try:
            with open('learned_data.json', 'r') as f:
                return json.load(f)
        except:
            return {"patterns": {}, "facts": []}

    def analyze_sentiment(self, text):
        result = self.sentiment_analyzer(text)[0]
        return result['label'], result['score']

    def summarize_text(self, text):
        return self.summarizer(text, max_length=130, min_length=30)[0]['summary_text']

    def answer_question(self, context, question):
        result = self.qa_model(question=question, context=context)
        return result['answer'], result['score']

    def learn_pattern(self, input_text, response):
        self.learned_responses["patterns"][input_text] = {
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "usage_count": 0
        }
        self._save_learned_data()

    def learn_fact(self, fact):
        self.learned_responses["facts"].append({
            "fact": fact,
            "timestamp": datetime.now().isoformat(),
            "source": "user"
        })
        self._save_learned_data()

    def generate_response(self, input_text):
        # Check learned patterns first
        if input_text in self.learned_responses["patterns"]:
            pattern = self.learned_responses["patterns"][input_text]
            pattern["usage_count"] += 1
            return pattern["response"]

        # Generate new response using DialoGPT
        input_ids = self.tokenizer.encode(input_text + self.tokenizer.eos_token, return_tensors='pt')
        chat_response_ids = self.chat_model.generate(
            input_ids,
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
            temperature=0.7
        )
        response = self.tokenizer.decode(chat_response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        self.conversation_history.append({"input": input_text, "response": response})
        return response

    def _save_learned_data(self):
        with open('learned_data.json', 'w') as f:
            json.dump(self.learned_responses, f, indent=2)
