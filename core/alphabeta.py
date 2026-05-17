from . import heuristic
from . import formation


nodes_visited = 0
branches_pruned = 0


def alphabeta(
    my_formation,
    opponent_formation,
    depth,
    alpha,
    beta,
    maximizing
):

    global nodes_visited
    global branches_pruned

    nodes_visited += 1

    # Terminal
    if depth == 0:

        score = heuristic.evaluate_state(
            my_formation,
            opponent_formation
        )

        return score, my_formation

    all_formations = formation.generate_all_formations(
        top_side=maximizing
    )

    # LIMIT SEARCH
    all_formations = all_formations[:40]

    # MAX
    if maximizing:

        best_formation = None
        best_score = float("-inf")

        for candidate in all_formations:

            score, _ = alphabeta(
                candidate,
                opponent_formation,
                depth - 1,
                alpha,
                beta,
                False
            )

            if score > best_score:

                best_score = score
                best_formation = candidate

            alpha = max(
                alpha,
                best_score
            )

            # PRUNE
            if beta <= alpha:

                branches_pruned += 1
                break

        return best_score, best_formation

    # MIN
    else:

        best_formation = None
        best_score = float("inf")

        for candidate in all_formations:

            score, _ = alphabeta(
                my_formation,
                candidate,
                depth - 1,
                alpha,
                beta,
                True
            )

            if score < best_score:

                best_score = score
                best_formation = candidate

            beta = min(
                beta,
                best_score
            )

            # PRUNE
            if beta <= alpha:

                branches_pruned += 1
                break

        return best_score, best_formation