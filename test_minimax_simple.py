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
    print("Kiểm tra Minimax depth=2")
    print("=" * 50)

    # Kiểm tra với 3 hình thức đội hình đối phương khác nhau
    strategy = MinimaxDepth2Strategy()

    # Kiểm tra 1: Đối phương có Tank, Mage, Assassin
    print("\nKiểm tra 1: Hình thức đội hình đối phương")
    opponent1 = [
        models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 2))
    ]
    print_formation(opponent1, "Đối phương")

    random.seed(42)
    ai_formation1 = strategy.choose_formation(opponent_formation=opponent1, top_side=True)
    print_formation(ai_formation1, "Đề xuất của AI (Minimax depth=2)")

    score1 = heuristic.eval(ai_formation1, opponent1)
    print("Điểm số heuristic (lợi thế của AI): {:.2f}".format(score1))
    print()

    # Kiểm tra 2: Đối phương có Warrior, Archer, Tank
    print("\nKiểm tra 2: Hình thức đội hình đối phương")
    opponent2 = [
        models.FormationUnit(piece=pieces.create_piece("Warrior"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Archer"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(2, 2))
    ]
    print_formation(opponent2, "Đối phương")

    random.seed(123)
    ai_formation2 = strategy.choose_formation(opponent_formation=opponent2, top_side=True)
    print_formation(ai_formation2, "Đề xuất của AI (Minimax depth=2)")

    score2 = heuristic.eval(ai_formation2, opponent2)
    print("Điểm số heuristic (lợi thế của AI): {:.2f}".format(score2))
    print()

    # Kiểm tra 3: Đối phương có Mage, Assassin, Archer
    print("\nKiểm tra 3: Hình thức đội hình đối phương")
    opponent3 = [
        models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Archer"), position=models.Position(2, 2))
    ]
    print_formation(opponent3, "Đối phương")

    random.seed(456)
    ai_formation3 = strategy.choose_formation(opponent_formation=opponent3, top_side=True)
    print_formation(ai_formation3, "Đề xuất của AI (Minimax depth=2)")

    score3 = heuristic.eval(ai_formation3, opponent3)
    print("Điểm số heuristic (lợi thế của AI): {:.2f}".format(score3))
    print()

    print("Tóm tắt các đề xuất của AI:")
    print("- Kiểm tra 1: AI đấu với Tank/Mage/Assassin")
    print("- Kiểm tra 2: AI đấu với Warrior/Archer/Tank")
    print("- Kiểm tra 3: AI đấu với Mage/Assassin/Archer")

if __name__ == "__main__":
    main()