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
            "- Bảo vệ tuyến trước bằng Tank"
        )

    # Assassin
    if "Assassin" in names:

        lines.append(
            "- Assassin có thể tiêu diệt mục tiêu mỏng manh"
        )

    # Mage
    if "Mage" in names:

        lines.append(
            "- Mage cung cấp sát thương burst cao"
        )

    # Archer
    if "Archer" in names:

        lines.append(
            "- Archer cung cấp DPS tầm xa cân bằng"
        )

    # Warrior
    if "Warrior" in names:

        lines.append(
            "- Warrior tăng khả năng sinh tồn"
        )

    # Diversity
    unique_types = len(
        set(names)
    )

    if unique_types >= 3:

        lines.append(
            "- Thành phần đội cân bằng"
        )

    return lines