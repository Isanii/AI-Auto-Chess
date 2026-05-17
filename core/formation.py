import random
import itertools

from . import constants
from . import models
from . import pieces

MAX_FORMATIONS = 300
def generate_random_formation(
    top_side: bool = True
) -> models.Formation:

    if top_side:
        valid_rows = [0, 1]
    else:
        valid_rows = [2, 3]

    positions = [
        (r, c)
        for r in valid_rows
        for c in range(constants.BOARD_SIZE)
    ]

    selected_positions = random.sample(
        positions,
        constants.TEAM_SIZE
    )

    formation = []

    for row, col in selected_positions:

        piece_name = random.choice(
            pieces.get_all_piece_names()
        )

        piece = pieces.create_piece(
            piece_name
        )

        unit = models.FormationUnit(
            piece=piece,
            position=models.Position(row, col)
        )

        formation.append(unit)

    return formation


def generate_all_formations(
    top_side: bool = True,
    limit: int = MAX_FORMATIONS
):

    if top_side:
        valid_rows = [0, 1]
    else:
        valid_rows = [2, 3]

    positions = [
        (r, c)
        for r in valid_rows
        for c in range(constants.BOARD_SIZE)
    ]

    piece_names = pieces.get_all_piece_names()

    all_formations = []

    attempts = 0

    while len(all_formations) < limit:

        attempts += 1

        selected_positions = random.sample(
            positions,
            constants.TEAM_SIZE
        )

        formation_units = []

        for row, col in selected_positions:

            piece_name = random.choice(
                piece_names
            )

            piece = pieces.create_piece(
                piece_name
            )

            formation_units.append(
                models.FormationUnit(
                    piece=piece,
                    position=models.Position(
                        row,
                        col
                    )
                )
            )

        all_formations.append(
            formation_units
        )

    return all_formations