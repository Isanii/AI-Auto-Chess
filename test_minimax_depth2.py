import sys
sys.path.insert(0, '.')

from core import constants, models, heuristic, pieces, formation
from core.strategies import MinimaxDepth2Strategy
import copy

# Backup original piece stats
original_piece_stats = copy.deepcopy(constants.PIECE_STATS)

def test_team(team_name, piece_names):
    """Test minimax with a specific team composition"""
    print(f"\n=== Testing {team_name} ===")
    print(f"Available pieces: {', '.join(piece_names)}")

    # Modify constants to only include these pieces
    constants.PIECE_STATS = {
        name: original_piece_stats[name]
        for name in piece_names if name in original_piece_stats
    }

    # Clear any cached piece names if needed
    # (get_all_piece_names reads from constants.PIECE_STATS directly)

    try:
        # Create strategy
        strategy = MinimaxDepth2Strategy()

        # Generate a random opponent formation (using same piece set)
        opponent_formation = formation.generate_random_formation(top_side=False)

        # Get AI's recommended formation
        recommenced_formation = strategy.choose_formation(
            opponent_formation=opponent_formation,
            top_side=True
        )

        # Display results
        print(f"Opponent formation:")
        for i, unit in enumerate(opponent_formation):
            print(f"  Unit {i+1}: {unit.piece.name} at ({unit.position.row}, {unit.position.col})")

        print(f"AI's recommended formation:")
        for i, unit in enumerate(recommenced_formation):
            print(f"  Unit {i+1}: {unit.piece.name} at ({unit.position.row}, {unit.position.col})")

        # Calculate heuristic score
        score = heuristic.eval(recommenced_formation, opponent_formation)
        print(f"Heuristic score (AI advantage): {score:.2f}")

    except Exception as e:
        print(f"Error testing {team_name}: {e}")
    finally:
        # Restore original piece stats
        constants.PIECE_STATS = original_piece_stats

def main():
    print("Kiểm tra Minimax depth=2")

    # Kiểm tra với 3 hình thức đội hình đối thủ khác nhau như trong ví dụ Test Counter-Picking
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

    strategy = MinimaxDepth2Strategy()

    for test_name, opponent_formation in test_cases:
        print(f"\n{test_name}")
        print("-" * 40)

        # Thiết lập hạt cho khả năng tái tạo (sử dụng hash đơn giản của test_name)
        seed = hash(test_name) % 1000
        random.seed(seed)
        ai_formation = strategy.choose_formation(opponent_formation=opponent_formation, top_side=True)

        # Hiển thị đội hình đối phương
        print("Đội hình Kẻ thù (Bên trên):")
        for i, unit in enumerate(opponent_formation):
            print(f"  {i+1}. {unit.piece.name} at ({unit.position.row}, {unit.position.col})")
        print()

        # Hiển thị đề xuất của AI
        print("Đề xuất của AI (Minimax depth=2) (Bên dưới):")
        for i, unit in enumerate(ai_formation):
            print(f"  {i+1}. {unit.piece.name} at ({unit.position.row}, {unit.position.col})")
        print()

        # Tính và hiển thị điểm số heuristic
        score = heuristic.eval(ai_formation, opponent_formation)
        print(f"Điểm số heuristic (lợi thế của AI): {score:.2f}")
        print("(Điểm số dương có nghĩa là AI có lợi thế)")

        # Hiển thị cũng những quân được sử dụng
        ai_pieces = [unit.piece.name for unit in ai_formation]
        opp_pieces = [unit.piece.name for unit in opponent_formation]
        print(f"AI sử dụng: {', '.join(ai_pieces)}")
        print(f"Kẻ thù sử dụng: {', '.join(opp_pieces)}")

if __name__ == "__main__":
    main()