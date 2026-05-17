from . import heuristic
from . import formation


nodes_visited = 0


def minimax(
    my_formation,
    opponent_formation,
    depth,
    maximizing
):

    global nodes_visited

    nodes_visited += 1

    # Terminal state
    if depth == 0:

        score = heuristic.evaluate_state(
            my_formation,
            opponent_formation
        )

        return score, my_formation

    all_formations = formation.generate_all_formations(
        top_side=maximizing
    )

    # LIMIT SEARCH SPACE
    all_formations = all_formations[:120]

    # MAX PLAYER
    if maximizing:

        best_score = float("-inf")
        best_formation = None

        for candidate in all_formations:

            score, _ = minimax(
                candidate,
                opponent_formation,
                depth - 1,
                False
            )

            if score > best_score:

                best_score = score
                best_formation = candidate

        return best_score, best_formation

    # MIN PLAYER
    else:

        best_score = float("inf")
        best_formation = None

        for candidate in all_formations:

            score, _ = minimax(
                my_formation,
                candidate,
                depth - 1,
                True
            )

            if score < best_score:

                best_score = score
                best_formation = candidate

        return best_score, best_formation