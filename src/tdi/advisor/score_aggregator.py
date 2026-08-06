from tdi.advisor.rule_result import RuleResult


class ScoreAggregator:

    @staticmethod
    def compute(results):
        return sum(r.score for r in results)

    @staticmethod
    def max_score(results):
        """Retourne le score maximal théorique."""
        return sum(r.max_score for r in results)

    @staticmethod
    def normalized_score(results):
        """Retourne le score global normalisé sur 100."""
        maximum = ScoreAggregator.max_score(results)

        if maximum == 0:
            return 0

        score = ScoreAggregator.compute(results)
        return round((score / maximum) * 100)

    @staticmethod
    def strengths(results):
        return [
            r.message
            for r in results
            if r.passed
        ]

    @staticmethod
    def weaknesses(results):
        return [
            r.message
            for r in results
            if not r.passed
        ]

    @staticmethod
    def score_by_category(results):
        """Retourne le score obtenu et maximal pour chaque catégorie."""
        categories = {}

        for result in results:
            category = result.category

            if category not in categories:
                categories[category] = {
                    "score": 0,
                    "max_score": 0,
            }

            categories[category]["score"] += result.score
            categories[category]["max_score"] += result.max_score

        return categories

    