from . import combat
from . import strategies


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

    return (
        all_strategies,
        standings,
        matrix
    )