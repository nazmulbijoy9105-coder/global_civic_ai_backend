from typing import List, Dict
import random

class AdaptivePsychometricEngine:
    """
    Adaptive psychometric engine with full Responsible AI audit factor integration.
    Includes adaptive question branching, confidence, and ethical/compliance scoring.
    """

    # Weight of each Responsible AI factor (sum=1)
    RESPONSIBLE_AI_FACTORS = {
        "bias_mitigation": 0.2,       # fairness & audit score
        "privacy_protection": 0.2,    # privacy enforcement
        "transparency": 0.15,         # explainability
        "psychological_safety": 0.15, # growth-oriented framing
        "governance": 0.1,            # risk & governance
        "general_quality": 0.2         # raw psychometric confidence
    }

    def __init__(self, question_bank: Dict[str, List[Dict]]):
        self.question_bank = question_bank
        self.user_responses = {}
        self.trait_scores = {}
        self.trait_confidence = {}
        self.trait_ai_scores = {}  # final ethically weighted scores
        self.audit_factors = {}    # per-trait audit scores

    def start_session(self):
        self.user_responses = {}
        self.trait_scores = {trait: 0 for trait in self.question_bank}
        self.trait_confidence = {trait: 1.0 for trait in self.question_bank}
        self.trait_ai_scores = {trait: 0 for trait in self.question_bank}
        # Initialize audit factors (0-1)
        self.audit_factors = {
            trait: {
                "bias_mitigation": 1.0,
                "privacy_protection": 1.0,
                "transparency": 1.0,
                "psychological_safety": 1.0,
                "governance": 1.0
            } for trait in self.question_bank
        }

    def set_audit_factors(self, trait: str, factors: Dict[str, float]):
        """
        Inject Responsible AI audit scores for a trait.
        Factors must be 0-1
        """
        if trait in self.audit_factors:
            for key, value in factors.items():
                if key in self.audit_factors[trait]:
                    self.audit_factors[trait][key] = max(0, min(1, value))

    def answer_question(self, trait: str, question_id: int, score: float):
        """
        Record user answer, update trait score and confidence
        """
        if trait not in self.user_responses:
            self.user_responses[trait] = []

        self.user_responses[trait].append({"question_id": question_id, "score": score})
        self.trait_scores[trait] += score

        # Update confidence: less variance → higher confidence
        answers = [r["score"] for r in self.user_responses[trait]]
        if len(answers) > 1:
            mean = sum(answers) / len(answers)
            variance = sum((x - mean) ** 2 for x in answers) / len(answers)
            self.trait_confidence[trait] = max(0.1, 1 - variance / 4)

    def next_question(self, trait: str) -> Dict:
        """
        Return next question for trait based on confidence
        """
        if trait not in self.question_bank:
            return {}

        confidence = self.trait_confidence.get(trait, 1.0)
        if confidence < 0.7:
            remaining = [q for q in self.question_bank[trait]
                         if q["id"] not in [r["question_id"] for r in self.user_responses.get(trait, [])]]
            if not remaining:
                return {}
            remaining.sort(key=lambda q: q.get("weight", 1), reverse=True)
            return remaining[0]
        else:
            return {}

    def finalize_trait_score(self, trait: str) -> float:
        """
        Normalize trait score with confidence and Responsible AI audit integration
        """
        num_questions = len(self.user_responses.get(trait, []))
        if num_questions == 0:
            return 0

        raw_score = self.trait_scores[trait] / num_questions
        confidence = self.trait_confidence.get(trait, 1.0)

        # Combine raw confidence with Responsible AI audit factors
        factors = self.audit_factors.get(trait, {})
        weighted_score = (
            factors.get("bias_mitigation", 1.0) * self.RESPONSIBLE_AI_FACTORS["bias_mitigation"] +
            factors.get("privacy_protection", 1.0) * self.RESPONSIBLE_AI_FACTORS["privacy_protection"] +
            factors.get("transparency", 1.0) * self.RESPONSIBLE_AI_FACTORS["transparency"] +
            factors.get("psychological_safety", 1.0) * self.RESPONSIBLE_AI_FACTORS["psychological_safety"] +
            factors.get("governance", 1.0) * self.RESPONSIBLE_AI_FACTORS["governance"] +
            confidence * self.RESPONSIBLE_AI_FACTORS["general_quality"]
        )

        final_score = raw_score * weighted_score
        self.trait_ai_scores[trait] = round(final_score, 2)
        return round(final_score, 2)

    def generate_report(self) -> Dict[str, float]:
        """
        Returns final report with Responsible AI audit-integrated scores
        """
        report = {}
        for trait in self.question_bank:
            report[trait] = self.finalize_trait_score(trait)
        return report
