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
    print("Kiểm tra Minimax depth=2")
    print("=" * 50)

    # Kiểm tra với 3 hình thức đội hình đối thủ khác nhau (mô phỏng các bộ quân khác nhau)
    # Vì chúng ta chỉ có 5 loại quân, chúng ta sẽ tạo ra các đội hình đối thủ khác nhau

    strategy = MinimaxDepth2Strategy()

    # Test 1: Đối phương có Tank, Mage, Assassin
    print("\nTest 1: Hình thức đội hình đối phương")
    opponent1 = [
        models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 2))
    ]
    print_formation(opponent1, "Đối phương")

    # Thiết lập hạt cho khả năng tái tạo
    random.seed(42)
    ai_formation1 = strategy.choose_formation(opponent_formation=opponent1, top_side=True)
    print_formation(ai_formation1, "Đề xuất của AI (Minimax depth=2)")

    score1 = heuristic.eval(ai_formation1, opponent1)
    print(f"Điểm số heuristic (lợi thế của AI): {score1:.2f}\n")

    # Test 2: Đối phương có Warrior, Archer, Tank
    print("\nTest 2: Hình thức đội hình đối phương")
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
    print(f"Điểm số heuristic (lợi thế của AI): {score2:.2f}\n")

    # Test 3: Đối phương có Mage, Assassin, Archer
    print("\nTest 3: Hình thức đội hình đối phương")
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
    print(f"Điểm số heuristic (lợi thế của AI): {score3:.2f}\n")

    print("Tóm tắt các đề xuất của AI:")
    print("- Test 1: AI đấu với Tank/Mage/Assassin")
    print("- Test 2: AI đấu với Warrior/Archer/Tank")
    print("- Test 3: AI đấu với Mage/Assassin/Archer")

if __name__ == "__main__":
    main()