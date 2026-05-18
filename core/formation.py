import random
import itertools

from . import constants
from . import models
from . import pieces

def generate_random_formation(
    top_side: bool = True
) -> models.Formation:

    if top_side:
        valid_rows = [0, 1]
    else:
        valid_rows = [constants.BOARD_SIZE-2, constants.BOARD_SIZE-1]

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
    limit: int = 200
):

    if top_side:
        valid_rows = [0, 1]
    else:
        valid_rows = [constants.BOARD_SIZE-2, constants.BOARD_SIZE-1]

    positions = [
        (r, c)
        for r in valid_rows
        for c in range(constants.BOARD_SIZE)
    ]

    piece_names = pieces.get_all_piece_names()

    all_formations = []

    # Generate all combinations of 3 positions
    for pos_combo in itertools.combinations(positions, constants.TEAM_SIZE):
        # For each combination, assign pieces (with repetition)
        for piece_combo in itertools.product(piece_names, repeat=constants.TEAM_SIZE):
            formation_units = []
            for (row, col), piece_name in zip(pos_combo, piece_combo):
                piece = pieces.create_piece(piece_name)
                unit = models.FormationUnit(
                    piece=piece,
                    position=models.Position(row, col)
                )
                formation_units.append(unit)
            all_formations.append(formation_units)
            if limit is not None and len(all_formations) >= limit:
                return all_formations

    return all_formations