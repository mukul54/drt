from typing import List, Dict
import json

class FeedbackIntegrator:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.feedback_data = []

    def add_feedback(self, challenge: str, response: str, risk_analysis: Dict):
        feedback_entry = {
            "challenge": challenge,
            "response": response,
            "risk_analysis": risk_analysis,
            "improvement_suggestions": self._generate_suggestions(risk_analysis)
        }
        self.feedback_data.append(feedback_entry)

    def _generate_suggestions(self, risk_analysis: Dict) -> List[str]:
        suggestions = []
        for category, probability in enumerate(risk_analysis["risk_probabilities"]):
            if probability > 0.5:
                suggestions.append(f"Address vulnerability in category {category}")
        if risk_analysis["severity_score"] > 0.7:
            suggestions.append("High severity issue detected. Prioritize for immediate attention.")
        return suggestions

    def generate_report(self):
        with open(self.output_file, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)
        print(f"Feedback report generated and saved to {self.output_file}")