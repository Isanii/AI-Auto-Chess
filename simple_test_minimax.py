import sys
sys.path.insert(0, '.')

from core import formation, heuristic, pieces, models
from core.strategies import MinimaxDepth2Strategy
import random

def print_formation(formation, label):
    print(f"{label}:")
    for i, unit in enumerate(formation):
        print(f"  {i+1}. {unit.piece.name} at ({unit.position.row}, {unit.position.col})")
    print()

def main():
    print("Testing Minimax depth=2")
    print("=" * 50)

    # Test with 3 different opponent formations (simulating different team compositions)
    # Since we only have 5 piece types, we'll create different opponent formations

    strategy = MinimaxDepth2Strategy()

    # Test 1: Opponent with Tank, Mage, Assassin
    print("\nTest 1: Opponent formation")
    opponent1 = [
        models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 2))
    ]
    print_formation(opponent1, "Opponent")

    # Set seed for reproducibility
    random.seed(42)
    ai_formation1 = strategy.choose_formation(opponent_formation=opponent1, top_side=True)
    print_formation(ai_formation1, "AI Recommendation (Minimax depth=2)")

    score1 = heuristic.eval(ai_formation1, opponent1)
    print(f"Heuristic score (AI advantage): {score1:.2f}\n")

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
    print(f"Heuristic score (AI advantage): {score2:.2f}\n")

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
    print(f"Heuristic score (AI advantage): {score3:.2f}\n")

    print("Summary of AI recommendations:")
    print("- Test 1: AI vs Tank/Mage/Assassin")
    print("- Test 2: AI vs Warrior/Archer/Tank")
    print("- Test 3: AI vs Mage/Assassin/Archer")

if __name__ == "__main__":
    main()