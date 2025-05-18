import numpy as np
from typing import List, Dict, Tuple


def calculate_cohens_kappa(rater1_scores: List[Dict[str, int]],
                           rater2_scores: List[Dict[str, int]],
                           criteria: List[str],
                           possible_ratings: List[int] = [1, 2, 3, 4, 5]) -> Dict[str, float]:

    def create_confusion_matrix(scores1: List[int], scores2: List[int], n_categories: int) -> np.ndarray:
        #Create a confusion matrix from two sets of ratings
        matrix = np.zeros((n_categories, n_categories))
        for s1, s2 in zip(scores1, scores2):
            matrix[s1 - 1][s2 - 1] += 1
        return matrix

    def calculate_kappa(matrix: np.ndarray) -> float:
        #Calculate Cohen's Kappa from a confusion matrix
        n = np.sum(matrix)
        if n == 0:
            return 0.0

        # Observed agreement
        po = np.sum(np.diag(matrix)) / n

        # Expected agreement by chance
        row_sums = np.sum(matrix, axis=1)
        col_sums = np.sum(matrix, axis=0)
        pe = np.sum(row_sums * col_sums) / (n * n)

        # Calculate kappa
        if pe == 1:
            return 1.0
        kappa = (po - pe) / (1 - pe)
        return kappa

    results = {}
    n_categories = len(possible_ratings)

    for criterion in criteria:
        scores1 = [r[criterion] for r in rater1_scores]
        scores2 = [r[criterion] for r in rater2_scores]

        matrix = create_confusion_matrix(scores1, scores2, n_categories)

        kappa = calculate_kappa(matrix)
        results[criterion] = kappa

    return results

def average_score(rater_1, rater_2, criterion):
    scores1 = [r[criterion] for r in rater1_scores]
    scores2 = [r[criterion] for r in rater2_scores]
    avrg = np.mean(scores1 + scores2)
    return avrg

if __name__ == "__main__":
    criteria = ["pattern_implementation_quality", "code_readability", "overall_improvement"]

    rater1_scores = [
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 2, "code_readability": 5, "overall_improvement": 3},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 2, "code_readability": 5, "overall_improvement": 3},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 2, "code_readability": 5, "overall_improvement": 3},
        {"pattern_implementation_quality": 2, "code_readability": 5, "overall_improvement": 3},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 4, "overall_improvement": 4},
        {"pattern_implementation_quality": 2, "code_readability": 5, "overall_improvement": 3},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5}
    ]

    rater2_scores = [
        {"pattern_implementation_quality": 3, "code_readability": 4, "overall_improvement": 4},
        {"pattern_implementation_quality": 2, "code_readability": 5, "overall_improvement": 3},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 3, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 2, "code_readability": 5, "overall_improvement": 3},
        {"pattern_implementation_quality": 3, "code_readability": 3, "overall_improvement": 3},
        {"pattern_implementation_quality": 4, "code_readability": 4, "overall_improvement": 4},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 3, "code_readability": 5, "overall_improvement": 4},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5},
        {"pattern_implementation_quality": 5, "code_readability": 5, "overall_improvement": 5}
    ]

    kappa_results = calculate_cohens_kappa(rater1_scores, rater2_scores, criteria)

    # Print results with interpretation
    for criterion, kappa in kappa_results.items():
        print(f"\nCriterion: {criterion}")
        print(f"Cohen's Kappa: {kappa:.3f}")
        print(f"Average Score: {average_score(rater1_scores, rater2_scores, criterion)}")

        if kappa <= 0:
            interpretation = "Poor agreement"
        elif kappa <= 0.20:
            interpretation = "Slight agreement"
        elif kappa <= 0.40:
            interpretation = "Fair agreement"
        elif kappa <= 0.60:
            interpretation = "Moderate agreement"
        elif kappa <= 0.80:
            interpretation = "Substantial agreement"
        else:
            interpretation = "Almost perfect agreement"

        print(f"Interpretation: {interpretation}")