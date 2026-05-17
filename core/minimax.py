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

        score = heuristic.eval(
            my_formation,
            opponent_formation
        )

        return score, my_formation

    # Generate formations for the side corresponding to the current player:
    # maximizing=True -> we are the player (bottom side) -> top_side=False
    # maximizing=False -> we are the opponent (top side) -> top_side=True
    all_formations = formation.generate_all_formations(
        top_side=not maximizing
    )

    # MAX PLAYER (we are maximizing)
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

    # MIN PLAYER (opponent is minimizing)
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