import random

from . import formation
from . import heuristic
from . import minimax
from . import alphabeta



class BaseStrategy:

    def __init__(self, name):

        self.name = name

    def choose_formation(
        self,
        opponent_formation=None
    ):
        raise NotImplementedError


# RANDOM
class RandomStrategy(BaseStrategy):

    def __init__(self):

        super().__init__(
            "Random"
        )

    def choose_formation(
        self,
        opponent_formation=None
    ):

        return formation.generate_random_formation(
            top_side=True
        )


# GREEDY HP
class GreedyHPStrategy(BaseStrategy):

    def __init__(self):

        super().__init__(
            "GreedyHP"
        )

    def choose_formation(
        self,
        opponent_formation=None
    ):

        formations = formation.generate_all_formations(
            top_side=True
        )[:300]

        best_score = float("-inf")
        best_formation = None

        for candidate in formations:

            total_hp = sum(
                u.piece.hp
                for u in candidate
            )

            if total_hp > best_score:

                best_score = total_hp
                best_formation = candidate

        return best_formation


# GREEDY ATK
class GreedyATKStrategy(BaseStrategy):

    def __init__(self):

        super().__init__(
            "GreedyATK"
        )

    def choose_formation(
        self,
        opponent_formation=None
    ):

        formations = formation.generate_all_formations(
            top_side=True
        )[:300]

        best_score = float("-inf")
        best_formation = None

        for candidate in formations:

            total_atk = sum(
                u.piece.atk
                for u in candidate
            )

            if total_atk > best_score:

                best_score = total_atk
                best_formation = candidate

        return best_formation


# MINIMAX DEPTH 2
class MinimaxDepth2Strategy(BaseStrategy):

    def __init__(self):

        super().__init__(
            "MinimaxDepth2"
        )

    def choose_formation(
        self,
        opponent_formation=None
    ):

        if opponent_formation is None:

            opponent_formation = formation.generate_random_formation(
                top_side=False
            )
        minimax.nodes_visited = 0
        score, best_formation = minimax.minimax(
            my_formation=None,
            opponent_formation=opponent_formation,
            depth=2,
            maximizing=True
        )

        return best_formation


# MINIMAX DEPTH 3
class MinimaxDepth3Strategy(BaseStrategy):
    def __init__(self):

        super().__init__(
            "MinimaxDepth3"
        )

    def choose_formation(
        self,
        opponent_formation=None
    ):
        alphabeta.nodes_visited = 0
        alphabeta.branches_pruned = 0
        if opponent_formation is None:

            opponent_formation = formation.generate_random_formation(
                top_side=False
            )

        score, best_formation = alphabeta.alphabeta(
            my_formation=None,
            opponent_formation=opponent_formation,
            depth=2,
            alpha=float("-inf"),
            beta=float("inf"),
            maximizing=True
        )

        return best_formation


def get_all_strategies():

    return [

        RandomStrategy(),

        GreedyHPStrategy(),

        GreedyATKStrategy(),

        MinimaxDepth2Strategy(),

        MinimaxDepth3Strategy()
    ]