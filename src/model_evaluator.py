# model_evaluator.py

import openai
from typing import List, Dict

class ModelEvaluator:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = openai.OpenAI()

    def evaluate_challenge(self, challenge: str) -> Dict:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are an AI assistant responding to user queries."},
                {"role": "user", "content": challenge}
            ],
            max_tokens=200
        )
        return {
            "challenge": challenge,
            "response": response.choices[0].message.content.strip(),
            "metadata": {
                "tokens": response.usage.total_tokens,
                "model": self.model_name,
            }
        }

    def evaluate_batch(self, challenges: List[str]) -> List[Dict]:
        return [self.evaluate_challenge(challenge) for challenge in challenges]
    