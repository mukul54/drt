# main.py

import os
import time
import openai
from typing import List
from challenge_generator import ChallengeGenerator
from model_evaluator import ModelEvaluator
from risk_analyzer import RiskAnalyzer
from feedback_integrator import FeedbackIntegrator

# Set your OpenAI API key
# Set your OpenAI API key
openai.api_key = "xxxxxy"
os.environ['OPENAI_API_KEY']=openai.api_key

class CentralOrchestrator:
    def __init__(
            self, 
            challenge_generator: ChallengeGenerator, 
            model_evaluator: ModelEvaluator, 
            risk_analyzer: RiskAnalyzer, 
            feedback_integrator: FeedbackIntegrator,
            risk_categories: List[str],
            evaluation_interval: int = 3600
            ):  # Default to hourly evaluations
        
        self.challenge_generator = challenge_generator
        self.model_evaluator = model_evaluator
        self.risk_analyzer = risk_analyzer
        self.feedback_integrator = feedback_integrator
        self.risk_categories = risk_categories
        self.evaluation_interval = evaluation_interval

    def run(self):
        while True:
            self._run_evaluation_cycle()
            time.sleep(self.evaluation_interval)

    def _run_evaluation_cycle(self):
        print("Starting new evaluation cycle...")
        challenges = self.challenge_generator.generate_batch(self.risk_categories, batch_size=100)
        evaluation_results = self.model_evaluator.evaluate_batch(challenges)

        for result in evaluation_results:
            risk_analysis = self.risk_analyzer.analyze_response(result["response"])
            self.feedback_integrator.add_feedback(result["challenge"], result["response"], risk_analysis)

        self.feedback_integrator.generate_report()
        print("Evaluation cycle completed.")

if __name__ == "__main__":
    # Initialize components
    challenge_generator = ChallengeGenerator("gpt-3.5-turbo", vulnerability_db={})
    model_evaluator = ModelEvaluator("gpt-4")
    risk_analyzer = RiskAnalyzer(num_risk_categories=10)
    feedback_integrator = FeedbackIntegrator("drt_feedback_report.json")

    risk_categories = ["safety", "bias", "factual_accuracy", "privacy", "security"]

    # Create and run the orchestrator
    orchestrator = CentralOrchestrator(
        challenge_generator, 
        model_evaluator, 
        risk_analyzer, 
        feedback_integrator, 
        risk_categories
        )
    orchestrator.run()