from . import constants
from . import models


def calculate_unit_power(
    unit: models.FormationUnit
):

    piece = unit.piece

    # BASE STATS
    score = (
        piece.hp * 1.2
        +
        piece.atk * 2.0
        +
        piece.defense * 1.5
    )

    # POSITION BONUS
    score += constants.POSITION_BONUS[
        unit.position.row
    ][
        unit.position.col
    ] * 2

    # ROLE POSITION BONUS
    role = constants.ROLE_PREFERENCE[
        piece.name
    ]

    # FRONTLINE
    if role == "front":

        if unit.position.row in [0, 1]:

            score += 8

        else:

            score -= 5

    # BACKLINE
    elif role == "back":

        if unit.position.row in [2, 3]:

            score += 8

        else:

            score -= 5

    return score


def formation_spread_bonus(
    formation
):

    positions = [
        (
            u.position.row,
            u.position.col
        )
        for u in formation
    ]

    unique_positions = len(
        set(positions)
    )

    return unique_positions * 2


def team_balance_bonus(
    formation
):

    names = [
        u.piece.name
        for u in formation
    ]

    bonus = 0

    # HAS TANK
    if "Tank" in names:

        bonus += 5

    # HAS DAMAGE
    if (
        "Mage" in names
        or
        "Assassin" in names
    ):

        bonus += 5

    # MIXED TEAM
    unique_types = len(
        set(names)
    )

    bonus += unique_types * 2

    return bonus


def evaluate_formation(
    formation
):

    score = 0

    for unit in formation:

        score += calculate_unit_power(
            unit
        )

    score += formation_spread_bonus(
        formation
    )

    score += team_balance_bonus(
        formation
    )

    return score

def matchup_bonus(
    formation_a,
    formation_b
):

    bonus = 0

    for unit_a in formation_a:

        for unit_b in formation_b:

            # Assassin counter Mage
            if (
                unit_a.piece.name == "Assassin"
                and
                unit_b.piece.name == "Mage"
            ):

                bonus += 4

            # Mage counter Tank
            if (
                unit_a.piece.name == "Mage"
                and
                unit_b.piece.name == "Tank"
            ):

                bonus += 3

            # Tank weak against Mage
            if (
                unit_a.piece.name == "Tank"
                and
                unit_b.piece.name == "Mage"
            ):

                bonus -= 3

    return bonus

def evaluate_state(
    formation_a,
    formation_b
):

    score_a = evaluate_formation(
        formation_a
    )

    score_b = evaluate_formation(
        formation_b
    )

    matchup = matchup_bonus(
    formation_a,
    formation_b
    )

    return (
        score_a
        -
        score_b
        +
        matchup
    )