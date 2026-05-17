def explain_formation(
    formation
):

    lines = []

    names = [
        unit.piece.name
        for unit in formation
    ]

    # Tank
    if "Tank" in names:

        lines.append(
            "- Frontline protection with Tank"
        )

    # Assassin
    if "Assassin" in names:

        lines.append(
            "- Assassin can eliminate squishy targets"
        )

    # Mage
    if "Mage" in names:

        lines.append(
            "- Mage provides high burst damage"
        )

    # Archer
    if "Archer" in names:

        lines.append(
            "- Archer provides balanced ranged DPS"
        )

    # Warrior
    if "Warrior" in names:

        lines.append(
            "- Warrior adds survivability"
        )

    # Diversity
    unique_types = len(
        set(names)
    )

    if unique_types >= 3:

        lines.append(
            "- Balanced team composition"
        )

    return lines