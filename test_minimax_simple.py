import sys
sys.path.insert(0, '.')

from core import formation, heuristic, pieces, models
from core.strategies import MinimaxDepth2Strategy
import random

def print_formation(formation, label):
    print(label + ":")
    for i, unit in enumerate(formation):
        print("  {}. {} at ({}, {})".format(i+1, unit.piece.name, unit.position.row, unit.position.col))
    print()

def main():
    print("Testing Minimax depth=2")
    print("=" * 50)

    # Test with 3 different opponent formations
    strategy = MinimaxDepth2Strategy()

    # Test 1: Opponent with Tank, Mage, Assassin
    print("\nTest 1: Opponent formation")
    opponent1 = [
        models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 2))
    ]
    print_formation(opponent1, "Opponent")

    random.seed(42)
    ai_formation1 = strategy.choose_formation(opponent_formation=opponent1, top_side=True)
    print_formation(ai_formation1, "AI Recommendation (Minimax depth=2)")

    score1 = heuristic.eval(ai_formation1, opponent1)
    print("Heuristic score (AI advantage): {:.2f}".format(score1))
    print()

    # Test 2: Opponent with Warrior, Archer, Tank
    print("\nTest 2: Opponent formation")
    opponent2 = [
        models.FormationUnit(piece=pieces.create_piece("Warrior"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Archer"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(2, 2))
    ]
    print_formation(opponent2, "Opponent")

    random.seed(123)
    ai_formation2 = strategy.choose_formation(opponent_formation=opponent2, top_side=True)
    print_formation(ai_formation2, "AI Recommendation (Minimax depth=2)")

    score2 = heuristic.eval(ai_formation2, opponent2)
    print("Heuristic score (AI advantage): {:.2f}".format(score2))
    print()

    # Test 3: Opponent with Mage, Assassin, Archer
    print("\nTest 3: Opponent formation")
    opponent3 = [
        models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Archer"), position=models.Position(2, 2))
    ]
    print_formation(opponent3, "Opponent")

    random.seed(456)
    ai_formation3 = strategy.choose_formation(opponent_formation=opponent3, top_side=True)
    print_formation(ai_formation3, "AI Recommendation (Minimax depth=2)")

    score3 = heuristic.eval(ai_formation3, opponent3)
    print("Heuristic score (AI advantage): {:.2f}".format(score3))
    print()

    print("Summary of AI recommendations:")
    print("- Test 1: AI vs Tank/Mage/Assassin")
    print("- Test 2: AI vs Warrior/Archer/Tank")
    print("- Test 3: AI vs Mage/Assassin/Archer")

if __name__ == "__main__":
    main()