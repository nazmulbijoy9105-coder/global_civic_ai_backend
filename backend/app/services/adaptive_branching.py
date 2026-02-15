from typing import List, Dict
import random
import math


class AdaptivePsychometricEngine:
    """
    Adaptive psychometric engine with full Responsible AI audit factor integration.
    Includes:
    - Adaptive question branching
    - Variance-based confidence scoring
    - Proper raw score normalization
    - Multiplicative ethical multiplier
    - Explainable AI report output
    """

    # Weight of each Responsible AI factor (sum should = 1)
    RESPONSIBLE_AI_FACTORS = {
        "bias_mitigation": 0.2,
        "privacy_protection": 0.2,
        "transparency": 0.15,
        "psychological_safety": 0.15,
        "governance": 0.1,
        "general_quality": 0.2  # confidence weight
    }

    def __init__(self, question_bank: Dict[str, List[Dict]], min_score: float = 1.0, max_score: float = 5.0):
        """
        question_bank structure:
        {
            "trait_name": [
                {"id": 1, "text": "...", "weight": 1},
                ...
            ]
        }
        """
        self.question_bank = question_bank
        self.min_score = min_score
        self.max_score = max_score

        self.user_responses = {}
        self.trait_scores = {}
        self.trait_confidence = {}
        self.trait_ai_scores = {}
        self.audit_factors = {}

    def start_session(self):
        self.user_responses = {}
        self.trait_scores = {trait: 0 for trait in self.question_bank}
        self.trait_confidence = {trait: 1.0 for trait in self.question_bank}
        self.trait_ai_scores = {trait: 0 for trait in self.question_bank}

        # Initialize Responsible AI audit factors (default fully compliant)
        self.audit_factors = {
            trait: {
                "bias_mitigation": 1.0,
                "privacy_protection": 1.0,
                "transparency": 1.0,
                "psychological_safety": 1.0,
                "governance": 1.0
            }
            for trait in self.question_bank
        }

    def set_audit_factors(self, trait: str, factors: Dict[str, float]):
        """
        Inject Responsible AI audit scores (0-1 range).
        """
        if trait in self.audit_factors:
            for key, value in factors.items():
                if key in self.audit_factors[trait]:
                    self.audit_factors[trait][key] = max(0.0, min(1.0, value))

    def answer_question(self, trait: str, question_id: int, score: float):
        """
        Record user answer and update trait score + confidence.
        """
        if trait not in self.user_responses:
            self.user_responses[trait] = []

        self.user_responses[trait].append({
            "question_id": question_id,
            "score": score
        })

        self.trait_scores[trait] += score

        # Update confidence (variance-based)
        answers = [r["score"] for r in self.user_responses[trait]]

        if len(answers) > 1:
            mean = sum(answers) / len(answers)
            variance = sum((x - mean) ** 2 for x in answers) / len(answers)

            # Normalize variance impact (assuming 1-5 scale default)
            max_variance = ((self.max_score - self.min_score) ** 2) / 4
            normalized_variance = variance / max_variance if max_variance else 0

            self.trait_confidence[trait] = max(0.1, 1 - normalized_variance)

    def next_question(self, trait: str) -> Dict:
        """
        Return next high-weight question if confidence < threshold.
        """
        if trait not in self.question_bank:
            return {}

        confidence = self.trait_confidence.get(trait, 1.0)

        if confidence < 0.7:
            answered_ids = [
                r["question_id"]
                for r in self.user_responses.get(trait, [])
            ]

            remaining = [
                q for q in self.question_bank[trait]
                if q["id"] not in answered_ids
            ]

            if not remaining:
                return {}

            remaining.sort(key=lambda q: q.get("weight", 1), reverse=True)
            return remaining[0]

        return {}

    def normalize_raw_score(self, raw_score: float) -> float:
        """
        Normalize raw score into 0-1 scale.
        """
        if self.max_score == self.min_score:
            return 0.0

        normalized = (raw_score - self.min_score) / (self.max_score - self.min_score)
        return max(0.0, min(1.0, normalized))

    def calculate_ethical_multiplier(self, trait: str, confidence: float) -> float:
        """
        Multiplicative ethical integration:
        Π (factor ^ weight)
        """
        factors = self.audit_factors.get(trait, {})

        multiplier = 1.0

        for factor_name, weight in self.RESPONSIBLE_AI_FACTORS.items():
            if factor_name == "general_quality":
                value = confidence
            else:
                value = factors.get(factor_name, 1.0)

            multiplier *= math.pow(max(0.01, value), weight)

        return multiplier

    def finalize_trait_score(self, trait: str) -> Dict:
        """
        Compute final ethically integrated score.
        """
        responses = self.user_responses.get(trait, [])
        num_questions = len(responses)

        if num_questions == 0:
            return {
                "score": 0,
                "confidence": 0,
                "audit_profile": self.audit_factors.get(trait, {})
            }

        raw_average = self.trait_scores[trait] / num_questions
        normalized_score = self.normalize_raw_score(raw_average)

        confidence = self.trait_confidence.get(trait, 1.0)
        ethical_multiplier = self.calculate_ethical_multiplier(trait, confidence)

        final_score = normalized_score * ethical_multiplier
        final_score = round(final_score, 3)

        self.trait_ai_scores[trait] = final_score

        return {
            "score": final_score,
            "confidence": round(confidence, 3),
            "audit_profile": self.audit_factors.get(trait, {})
        }

    def generate_report(self) -> Dict[str, Dict]:
        """
        Generate full explainable Responsible AI report.
        """
        report = {}

        for trait in self.question_bank:
            report[trait] = self.finalize_trait_score(trait)

        return report