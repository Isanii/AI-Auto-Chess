import sys
sys.path.insert(0, '.')

from core import formation, heuristic, pieces, models
from core.counter_picker import find_best_counter

def print_formation(formation, label):
    print(f"{label}:")
    for i, unit in enumerate(formation):
        print(f"  {i+1}. {unit.piece.name} at ({unit.position.row}, {unit.position.col})")
    print()

def main():
    print("Testing Counter-Picking Strategy")
    print("=" * 50)

    # Test with 3 different opponent formations as requested
    test_cases = [
        ("Test 1 - Tank/Mage/Assassin", [
            models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(3, 0)),
            models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(2, 1)),
            models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 2))
        ]),
        ("Test 2 - Warrior/Archer/Tank", [
            models.FormationUnit(piece=pieces.create_piece("Warrior"), position=models.Position(3, 0)),
            models.FormationUnit(piece=pieces.create_piece("Archer"), position=models.Position(2, 1)),
            models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(2, 2))
        ]),
        ("Test 3 - Mage/Assassin/Archer", [
            models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(3, 0)),
            models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 1)),
            models.FormationUnit(piece=pieces.create_piece("Archer"), position=models.Position(2, 2))
        ])
    ]

    for test_name, opponent_formation in test_cases:
        print(f"\n{test_name}")
        print("-" * 40)
        print_formation(opponent_formation, "Opponent Formation (Top Side)")

        # Get AI's counter pick
        counter_formation, score = find_best_counter(opponent_formation)
        print_formation(counter_formation, "AI Counter Formation (Bottom Side)")

        # Show the heuristic score
        print(f"Counter-picking heuristic score: {score:.2f}")
        print(f"(Positive score means AI has advantage)")

        # Also show what pieces were used
        ai_pieces = [unit.piece.name for unit in counter_formation]
        opp_pieces = [unit.piece.name for unit in opponent_formation]
        print(f"AI used: {', '.join(ai_pieces)}")
        print(f"Opponent used: {', '.join(opp_pieces)}")

if __name__ == "__main__":
    main()