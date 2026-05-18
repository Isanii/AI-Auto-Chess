from . import combat
from . import strategies
from . import constants
import numpy as np
import copy


def run_match(
    strategy_a,
    strategy_b
):

    # Strategy A (Player) at BOTTOM (rows 2-3)
    formation_a = strategy_a.choose_formation(top_side=False)

    # Strategy B (Enemy) at TOP (rows 0-1)
    formation_b = strategy_b.choose_formation(
        formation_a,
        top_side=True
    )

    result = combat.simulate_battle(
        formation_a,
        formation_b
    )

    return result


def run_tournament():

    # Override constants for 5x5 board in tournament mode
    _ORIGINAL_BOARD_SIZE = constants.BOARD_SIZE
    _ORIGINAL_POSITION_BONUS = constants.POSITION_BONUS.copy()
    _ORIGINAL_FRONTLINE_ROWS = constants.FRONTLINE_ROWS.copy()
    _ORIGINAL_BACKLINE_ROWS = constants.BACKLINE_ROWS.copy()

    # Set 5x5 board specifications for tournament
    constants.BOARD_SIZE = 5
    constants.POSITION_BONUS = np.array([
        [0, 1, 1, 1, 0],
        [1, 2, 2, 2, 1],
        [1, 2, 3, 2, 1],
        [1, 2, 2, 2, 1],
        [0, 1, 1, 1, 0]
    ])
    constants.FRONTLINE_ROWS = [0, 1]  # First 2 rows
    constants.BACKLINE_ROWS = [3, 4]   # Last 2 rows (for 5x5: rows 3,4)

    all_strategies = strategies.get_all_strategies()

    standings = {}

    for strategy in all_strategies:

        standings[strategy.name] = {

            "wins": 0,

            "losses": 0,

            "draws": 0,

            "remaining_hp": 0,

            "total_turns": 0
        }

    matrix = []

    for strategy_a in all_strategies:

        row = []

        for strategy_b in all_strategies:

            if strategy_a.name == strategy_b.name:

                row.append("-")
                continue

            result = run_match(
                strategy_a,
                strategy_b
            )

            # TEAM A WIN
            if result.winner == "A":

                standings[
                    strategy_a.name
                ]["wins"] += 1

                standings[
                    strategy_b.name
                ]["losses"] += 1

                standings[
                    strategy_a.name
                ]["remaining_hp"] += (
                    result.remaining_hp_a
                )

                row.append("W")

            # TEAM B WIN
            elif result.winner == "B":

                standings[
                    strategy_b.name
                ]["wins"] += 1

                standings[
                    strategy_a.name
                ]["losses"] += 1

                standings[
                    strategy_b.name
                ]["remaining_hp"] += (
                    result.remaining_hp_b
                )

                row.append("L")

            # DRAW
            else:

                standings[
                    strategy_a.name
                ]["draws"] += 1

                standings[
                    strategy_b.name
                ]["draws"] += 1

                row.append("D")

            standings[
                strategy_a.name
            ]["total_turns"] += (
                result.turns
            )

            standings[
                strategy_b.name
            ]["total_turns"] += (
                result.turns
            )

        matrix.append(
            row
        )

    # Restore original constants
    constants.BOARD_SIZE = _ORIGINAL_BOARD_SIZE
    constants.POSITION_BONUS = _ORIGINAL_POSITION_BONUS
    constants.FRONTLINE_ROWS = _ORIGINAL_FRONTLINE_ROWS
    constants.BACKLINE_ROWS = _ORIGINAL_BACKLINE_ROWS

    return (
        all_strategies,
        standings,
        matrix
    )