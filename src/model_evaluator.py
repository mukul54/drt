import openai
from typing import List, Dict

class ModelEvaluator:
    def __init__(self, model_name: str):
        self.model = openai.Completion.create(engine=model_name)

    def evaluate_challenge(self, challenge: str) -> Dict:
        response = self.model.create(prompt=challenge, max_tokens=200)
        return {
            "challenge": challenge,
            "response": response.choices[0].text.strip(),
            "metadata": {
                "tokens": response.usage.total_tokens,
                "model": self.model.model,
            }
        }

    def evaluate_batch(self, challenges: List[str]) -> List[Dict]:
        return [self.evaluate_challenge(challenge) for challenge in challenges]