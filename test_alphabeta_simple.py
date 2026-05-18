import sys
import time
sys.path.insert(0, '.')

from core import formation, heuristic, pieces, models
from core import minimax
from core import alphabeta

def run_minimax(my_formation, opponent_formation, depth, maximizing=True):
    """Chạy minimax và trả về điểm số, đội hình, số nút đã thăm"""
    # Đặt lại bộ đếm
    minimax.nodes_visited = 0
    start_time = time.time()
    score, best_formation = minimax.minimax(
        my_formation, opponent_formation, depth, maximizing
    )
    end_time = time.time()
    return score, best_formation, minimax.nodes_visited, end_time - start_time

def run_alphabeta(my_formation, opponent_formation, depth, maximizing=True):
    """Chạy alpha-beta và trả về điểm số, đội hình, số nút đã thăm, số nhánh đã cắt"""
    # Đặt lại các bộ đếm
    alphabeta.nodes_visited = 0
    alphabeta.branches_pruned = 0
    start_time = time.time()
    score, best_formation = alphabeta.alphabeta(
        my_formation, opponent_formation, depth,
        float("-inf"), float("inf"), maximizing
    )
    end_time = time.time()
    return score, best_formation, alphabeta.nodes_visited, alphabeta.branches_pruned, end_time - start_time

def print_formation(formation, label):
    print(label + ":")
    for i, unit in enumerate(formation):
        print("  {}. {} at ({}, {})".format(i+1, unit.piece.name, unit.position.row, unit.position.col))
    print()

def main():
    print("So sánh Alpha-Beta Pruning vs Minimax")
    print("=" * 50)

    # Sử dụng đội hình đối thủ cố định để kiểm tra nhất quán
    opponent_formation = [
        models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 2))
    ]

    print("Đội hình Kẻ thù:")
    print_formation(opponent_formation, "Kẻ thù (Bên trên)")

    # Kiểm tra độ sâu 2 và 3
    for depth in [2, 3]:
        print("\n--- Độ sâu {} ---".format(depth))

        # Chạy Minimax
        print("Đang chạy Minimax...")
        score_min, form_min, nodes_min, time_min = run_minimax(
            None, opponent_formation, depth, maximizing=True
        )

        # Chạy Alpha-Beta
        print("Đang chạy Alpha-Beta...")
        score_ab, form_ab, nodes_ab, branches_ab, time_ab = run_alphabeta(
            None, opponent_formation, depth, maximizing=True
        )

        # Tính toán tiết kiệm
        if nodes_min > 0:
            reduction_pct = (1 - nodes_ab / nodes_min) * 100
        else:
            reduction_pct = 0

        time_saving = (1 - time_ab / time_min) * 100 if time_min > 0 else 0

        print("\nKết quả:")
        print("  Minimax:      Điểm={:.2f}, Nút={}, Thời gian={:.4f}s".format(score_min, nodes_min, time_min))
        print("  Alpha-Beta:   Điểm={:.2f}, Nút={}, Nhánh đã cắt={}, Thời gian={:.4f}s".format(score_ab, nodes_ab, branches_ab, time_ab))
        print("  Cải thiện:    Giảm nút {:.1f}%, Tiết kiệm thời gian {:.1f}%".format(reduction_pct, time_saving))

        # Kiểm tra điểm số có khớp nhau không (nên có với chơi hoàn hảo)
        if abs(score_min - score_ab) < 0.01:
            print("  Điểm số khớp")
        else:
            print("  Điểm số chênh lệch {:.2f}".format(abs(score_min - score_ab)))

        # Hiển thị đội hình AI
        print("\n  Đội hình AI Minimax:")
        print_formation(form_min, "")

        print("  Đội hình AI Alpha-Beta:")
        print_formation(form_ab, "")

if __name__ == "__main__":
    main()