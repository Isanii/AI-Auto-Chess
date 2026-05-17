from dataclasses import dataclass
from typing import List


@dataclass
class Piece:
    name: str
    atk: int
    defense: int
    hp: int


@dataclass
class Position:
    row: int
    col: int


@dataclass
class FormationUnit:
    piece: Piece
    position: Position


Formation = List[FormationUnit]

@dataclass
class BattleUnit:

    unit: FormationUnit

    current_hp: int

    alive: bool = True

@dataclass
class CombatEvent:

    attacker_team: str
    attacker_name: str

    attacker_row: int
    attacker_col: int

    defender_team: str
    defender_name: str

    defender_row: int
    defender_col: int

    damage: int

    defender_hp_before: int
    defender_hp_after: int

    defender_dead: bool

    turn: int

@dataclass
class BattleResult:

    winner: str

    remaining_hp_a: int
    remaining_hp_b: int

    turns: int

    combat_log: List[CombatEvent]