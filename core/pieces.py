from .models import Piece
from . import constants


def create_piece(name: str) -> Piece:

    if name not in constants.PIECE_STATS:
        raise ValueError(f"Unknown piece type: {name}")

    stats = constants.PIECE_STATS[name]

    return Piece(
        name=name,
        atk=stats["ATK"],
        defense=stats["DEF"],
        hp=stats["HP"]
    )


def get_all_piece_names():

    return list(
        constants.PIECE_STATS.keys()
    )