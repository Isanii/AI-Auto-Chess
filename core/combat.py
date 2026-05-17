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


def attack(
    attacker: models.BattleUnit,
    defender: models.BattleUnit
):

    damage_raw = attacker.unit.piece.atk - defender.unit.piece.defense
    damage = max(0, damage_raw)
    # Ensure minimum damage of 1 if attacker has positive attack
    if damage == 0 and attacker.unit.piece.atk > 0:
        damage = 1

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

    combat_log = []

    turn = 1

    # Prevent infinite battles
    zero_damage_turns = 0

    while turn <= constants.MAX_TURNS:

        # Reset zero damage counter at start of each turn
        zero_damage_turns = 0

        # TEAM A ATTACK
        for attacker in team_a:

            if not attacker.alive:
                continue

            target = choose_target(
                attacker,
                team_b
            )

            if target is None:
                break

            damage, hp_before = attack(
                attacker,
                target
            )

            # ZERO DAMAGE TRACKING
            if damage == 0:

                zero_damage_turns += 1

            else:

                zero_damage_turns = 0

            event = models.CombatEvent(

                attacker_team="A",
                attacker_name=attacker.unit.piece.name,

                attacker_row=attacker.unit.position.row,
                attacker_col=attacker.unit.position.col,

                defender_team="B",
                defender_name=target.unit.piece.name,

                defender_row=target.unit.position.row,
                defender_col=target.unit.position.col,

                damage=damage,

                defender_hp_before=hp_before,
                defender_hp_after=target.current_hp,

                defender_dead=not target.alive,

                turn=turn
            )

            combat_log.append(
                event
            )

        # TEAM B DEAD
        if not any(u.alive for u in team_b):

            return models.BattleResult(
                winner="A",

                remaining_hp_a=sum(
                    u.current_hp
                    for u in team_a
                ),

                remaining_hp_b=0,

                turns=turn,

                combat_log=combat_log
            )

        # TEAM B ATTACK
        for attacker in team_b:

            if not attacker.alive:
                continue

            target = choose_target(
                attacker,
                team_a
            )

            if target is None:
                break

            damage, hp_before = attack(
                attacker,
                target
            )

            # ZERO DAMAGE TRACKING
            if damage == 0:

                zero_damage_turns += 1

            else:

                zero_damage_turns = 0

            event = models.CombatEvent(

                attacker_team="B",
                attacker_name=attacker.unit.piece.name,

                attacker_row=attacker.unit.position.row,
                attacker_col=attacker.unit.position.col,

                defender_team="A",
                defender_name=target.unit.piece.name,

                defender_row=target.unit.position.row,
                defender_col=target.unit.position.col,

                damage=damage,

                defender_hp_before=hp_before,
                defender_hp_after=target.current_hp,

                defender_dead=not target.alive,

                turn=turn
            )

            combat_log.append(
                event
            )

        # TEAM A DEAD
        if not any(u.alive for u in team_a):

            return models.BattleResult(
                winner="B",

                remaining_hp_a=0,

                remaining_hp_b=sum(
                    u.current_hp
                    for u in team_b
                ),

                turns=turn,

                combat_log=combat_log
            )

        # INFINITE BATTLE PROTECTION
        # Only end battle if we had zero damage for ALL attacks in a turn
        if zero_damage_turns >= 20:  # 6 units * ~3-4 turns of zero damage

            return models.BattleResult(
                winner="Draw",

                remaining_hp_a=sum(
                    u.current_hp
                    for u in team_a
                ),

                remaining_hp_b=sum(
                    u.current_hp
                    for u in team_b
                ),

                turns=turn,

                combat_log=combat_log
            )

        turn += 1

    # DRAW
    return models.BattleResult(
        winner="Draw",

        remaining_hp_a=sum(
            u.current_hp
            for u in team_a
        ),

        remaining_hp_b=sum(
            u.current_hp
            for u in team_b
        ),

        turns=turn,

        combat_log=combat_log
    )