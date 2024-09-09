import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel
from typing import Dict

class RiskAnalyzer(nn.Module):
    def __init__(self, num_risk_categories: int):
        super().__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_risk_categories)
        self.severity_regressor = nn.Linear(self.bert.config.hidden_size, 1)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        risk_logits = self.classifier(pooled_output)
        severity_score = self.severity_regressor(pooled_output)
        return risk_logits, severity_score

    def analyze_response(self, response: str) -> Dict:
        inputs = self.tokenizer(response, return_tensors='pt', truncation=True, max_length=512)
        with torch.no_grad():
            risk_logits, severity_score = self(inputs['input_ids'], inputs['attention_mask'])
        
        risk_probs = torch.sigmoid(risk_logits)
        return {
            "risk_probabilities": risk_probs.squeeze().tolist(),
            "severity_score": severity_score.item()
        }