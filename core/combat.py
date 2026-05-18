import random

from . import models
from . import constants


def manhattan_distance(
    pos_a: models.Position,
    pos_b: models.Position
):

    return (
        abs(pos_a.row - pos_b.row)
        +
        abs(pos_a.col - pos_b.col)
    )


def choose_target(
    attacker: models.BattleUnit,
    defenders: list[models.BattleUnit]
):

    alive_defenders = [
        d for d in defenders
        if d.alive
    ]

    if not alive_defenders:
        return None

    candidates = []

    for defender in alive_defenders:

        distance = manhattan_distance(
            attacker.unit.position,
            defender.unit.position
        )

        candidates.append(
            (
                distance,
                defender.current_hp,
                defender.unit.piece.defense,
                random.random(),
                defender
            )
        )

    candidates.sort(
        key=lambda x: (
            x[0],
            x[1],
            x[2],
            x[3]
        )
    )

    return candidates[0][4]


def find_closest_pair(
    team_a: list[models.BattleUnit],
    team_b: list[models.BattleUnit]
):
    """Find the pair (a from team_a, b from team_b) with minimal Manhattan distance.
    Returns (a, b). If multiple pairs have same distance, the first encountered is returned."""
    min_dist = float('inf')
    best_pair = None
    for a in team_a:
        if not a.alive:
            continue
        for b in team_b:
            if not b.alive:
                continue
            dist = manhattan_distance(a.unit.position, b.unit.position)
            if dist < min_dist:
                min_dist = dist
                best_pair = (a, b)
    return best_pair


def attack(
    attacker: models.BattleUnit,
    defender: models.BattleUnit
):

    damage_raw = attacker.unit.piece.atk - defender.unit.piece.defense
    damage = max(0, damage_raw)

    hp_before = defender.current_hp

    defender.current_hp -= damage

    if defender.current_hp <= 0:

        defender.current_hp = 0
        defender.alive = False

    return damage, hp_before


def create_battle_team(
    formation: models.Formation
):

    team = []

    for formation_unit in formation:

        battle_unit = models.BattleUnit(
            unit=formation_unit,
            current_hp=formation_unit.piece.hp
        )

        team.append(
            battle_unit
        )

    return team


def simulate_battle(
    formation_a: models.Formation,
    formation_b: models.Formation
):

    team_a = create_battle_team(
        formation_a
    )

    team_b = create_battle_team(
        formation_b
    )

    # Early draw detection: if neither team can damage the other, it's a draw
    # Compute max ATK for each team and min DEF for the opposing team
    if team_a and team_b:
        max_atk_a = max(unit.unit.piece.atk for unit in team_a if unit.alive)
        max_atk_b = max(unit.unit.piece.atk for unit in team_b if unit.alive)
        min_def_b = min(unit.unit.piece.defense for unit in team_b if unit.alive)
        min_def_a = min(unit.unit.piece.defense for unit in team_a if unit.alive)
        # If both sides cannot inflict damage on the other, it's a perpetual block
        if max_atk_a <= min_def_b and max_atk_b <= min_def_a:
            # No damage possible from either side -> immediate draw
            remaining_hp_a = sum(unit.current_hp for unit in team_a)
            remaining_hp_b = sum(unit.current_hp for unit in team_b)
            return models.BattleResult(
                winner="Draw",
                remaining_hp_a=remaining_hp_a,
                remaining_hp_b=remaining_hp_b,
                turns=0,
                combat_log=[]
            )

    combat_log = []
    turn = 0  # even turns: A attacks, odd turns: B attacks
    max_turns = constants.MAX_TURNS * 2  # safety limit

    # Stalemate detection: if too many consecutive turns result in no HP change for either side
    consecutive_no_change = 0
    max_consecutive_no_change = 20  # Allow up to 20 turns with no change before considering stalemate
    prev_hp_a = sum(unit.current_hp for unit in team_a)
    prev_hp_b = sum(unit.current_hp for unit in team_b)

    while turn < max_turns:
        if turn % 2 == 0:
            # A's turn to attack
            if not any(u.alive for u in team_a) or not any(u.alive for u in team_b):
                break
            pair = find_closest_pair(team_a, team_b)
            if pair is None:
                break
            attacker, defender = pair
            damage, hp_before = attack(attacker, defender)
            event = models.CombatEvent(
                attacker_team="A",
                attacker_name=attacker.unit.piece.name,
                attacker_row=attacker.unit.position.row,
                attacker_col=attacker.unit.position.col,
                defender_team="B",
                defender_name=defender.unit.piece.name,
                defender_row=defender.unit.position.row,
                defender_col=defender.unit.position.col,
                damage=damage,
                defender_hp_before=hp_before,
                defender_hp_after=defender.current_hp,
                defender_dead=not defender.alive,
                turn=turn // 2  # full turn number (each full turn = A and B attack)
            )
            combat_log.append(event)
        else:
            # B's turn to attack
            if not any(u.alive for u in team_a) or not any(u.alive for u in team_b):
                break
            pair = find_closest_pair(team_b, team_a)
            if pair is None:
                break
            attacker, defender = pair
            damage, hp_before = attack(attacker, defender)
            event = models.CombatEvent(
                attacker_team="B",
                attacker_name=attacker.unit.piece.name,
                attacker_row=attacker.unit.position.row,
                attacker_col=attacker.unit.position.col,
                defender_team="A",
                defender_name=defender.unit.piece.name,
                defender_row=defender.unit.position.row,
                defender_col=defender.unit.position.col,
                damage=damage,
                defender_hp_before=hp_before,
                defender_hp_after=defender.current_hp,
                defender_dead=not defender.alive,
                turn=turn // 2
            )
            combat_log.append(event)

        # Check for stalemate: no HP change for both sides
        current_hp_a = sum(unit.current_hp for unit in team_a)
        current_hp_b = sum(unit.current_hp for unit in team_b)

        if current_hp_a == prev_hp_a and current_hp_b == prev_hp_b:
            consecutive_no_change += 1
        else:
            consecutive_no_change = 0  # Reset if HP changed
            prev_hp_a = current_hp_a
            prev_hp_b = current_hp_b

        # If too many consecutive turns with no HP change, declare draw
        if consecutive_no_change >= max_consecutive_no_change:
            remaining_hp_a = current_hp_a
            remaining_hp_b = current_hp_b
            total_turns = (turn + 1) // 2
            return models.BattleResult(
                winner="Draw",
                remaining_hp_a=remaining_hp_a,
                remaining_hp_b=remaining_hp_b,
                turns=total_turns,
                combat_log=combat_log
            )

        turn += 1

    # Determine winner
    alive_a = [u for u in team_a if u.alive]
    alive_b = [u for u in team_b if u.alive]
    if not alive_a and not alive_b:
        winner = "Draw"
    elif not alive_a:
        winner = "B"
    elif not alive_b:
        winner = "A"
    else:
        # Max turns reached
        winner = "Draw"

    remaining_hp_a = sum(u.current_hp for u in team_a)
    remaining_hp_b = sum(u.current_hp for u in team_b)
    total_turns = (turn + 1) // 2  # number of full turns completed

    return models.BattleResult(
        winner=winner,
        remaining_hp_a=remaining_hp_a,
        remaining_hp_b=remaining_hp_b,
        turns=total_turns,
        combat_log=combat_log
    )