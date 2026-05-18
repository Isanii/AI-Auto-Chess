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
    print("Kiểm tra Chiến Lượng Phụ")
    print("=" * 50)

    # Kiểm tra với 3 hình thức đội hình đối thủ khác nhau như yêu cầu
    test_cases = [
        ("Kiểm tra 1 - Tank/Mage/Assassin", [
            models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(3, 0)),
            models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(2, 1)),
            models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 2))
        ]),
        ("Kiểm tra 2 - Warrior/Archer/Tank", [
            models.FormationUnit(piece=pieces.create_piece("Warrior"), position=models.Position(3, 0)),
            models.FormationUnit(piece=pieces.create_piece("Archer"), position=models.Position(2, 1)),
            models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(2, 2))
        ]),
        ("Kiểm tra 3 - Mage/Assassin/Archer", [
            models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(3, 0)),
            models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 1)),
            models.FormationUnit(piece=pieces.create_piece("Archer"), position=models.Position(2, 2))
        ])
    ]

    for test_name, opponent_formation in test_cases:
        print(f"\n{test_name}")
        print("-" * 40)
        print_formation(opponent_formation, "Đội hình Kẻ thù (Bên trên)")

        # Lấy chiến lược phản công tốt nhất của AI
        counter_formation, score = find_best_counter(opponent_formation)
        print_formation(counter_formation, "Đội hình Phản công của AI (Bên dưới)")

        # Hiển thị điểm số heuristic
        print(f"Điểm số heuristic phản công: {score:.2f}")
        print(f"(Điểm số dương có nghĩa là AI có lợi thế)")

        # Hiển thị cũng những quân được sử dụng
        ai_pieces = [unit.piece.name for unit in counter_formation]
        opp_pieces = [unit.piece.name for unit in opponent_formation]
        print(f"AI sử dụng: {', '.join(ai_pieces)}")
        print(f"Kẻ thù sử dụng: {', '.join(opp_pieces)}")

if __name__ == "__main__":
    main()