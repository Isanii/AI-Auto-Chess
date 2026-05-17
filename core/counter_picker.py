from . import formation
from . import heuristic


def find_best_counter(
    opponent_formation
):

    candidates = formation.generate_all_formations(
        top_side=True,
        limit=150
    )

    best_score = float("-inf")
    best_formation = None

    for candidate in candidates:

        score = heuristic.evaluate_state(
            candidate,
            opponent_formation
        )

        if score > best_score:

            best_score = score
            best_formation = candidate

    return best_formation, best_score