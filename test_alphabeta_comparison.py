import sys
import time
sys.path.insert(0, '.')

from core import formation, heuristic
from core import minimax
from core import alphabeta

def run_minimax(my_formation, opponent_formation, depth, maximizing=True):
    """Chạy minimax và trả về điểm số, đội hình, số nút được visited"""
    # Reset counter
    minimax.nodes_visited = 0
    start_time = time.time()
    score, best_formation = minimax.minimax(
        my_formation, opponent_formation, depth, maximizing
    )
    end_time = time.time()
    return score, best_formation, minimax.nodes_visited, end_time - start_time

def run_alphabeta(my_formation, opponent_formation, depth, maximizing=True):
    """Chạy alpha-beta và trả về điểm số, đội hình, số nút được visited, số nhánh đã cắt"""
    # Reset counters
    alphabeta.nodes_visited = 0
    alphabeta.branches_pruned = 0
    start_time = time.time()
    score, best_formation = alphabeta.alphabeta(
        my_formation, opponent_formation, depth,
        float("-inf"), float("inf"), maximizing
    )
    end_time = time.time()
    return score, best_formation, alphabeta.nodes_visited, alphabeta.branches_pruned, end_time - start_time

def test_formation_comparison(team_name, piece_names):
    """Kiểm tra cả hai thuật toán với một cấu trúc đội cụ thể"""
    print(f"\n{'='*60}")
    print(f"Kiểm tra {team_name}")
    print(f"{'='*60}")

    # Sao lưu stats gốc của quân pieza
    original_piece_stats = {}
    for k, v in formation.constants.PIECE_STATS.items():
        original_piece_stats[k] = v.copy()

    try:
        # Sửa đổi constants để chỉ bao gồm các quân pieza này
        formation.constants.PIECE_STATS = {
            k: v for k, v in original_piece_stats.items()
            if k in piece_names
        }

        # Tạo đội hình đối phương cố định để kiểm tra nhất quán
        # Chúng ta sẽ sử dụng một編成 được preset thay vì random để có thể tái tạo
        opponent_formation = [
            formation.models.FormationUnit(
                piece=formation.pieces.create_piece("Tank"),
                position=formation.models.Position(3, 0)
            ),
            formation.models.FormationUnit(
                piece=formation.pieces.create_piece("Mage"),
                position=formation.models.Position(2, 1)
            ),
            formation.models.FormationUnit(
                piece=formation.pieces.create_piece("Assassin"),
                position=formation.models.Position(2, 2)
            )
        ]

        print(f"Đội hình đối phương (fixed):")
        for i, unit in enumerate(opponent_formation):
            print(f"  Unit {i+1}: {unit.piece.name} at ({unit.position.row}, {unit.position.col})")

        # Kiểm tra độ sâu 2 và 3
        for depth in [2, 3]:
            print(f"\n--- Độ sâu {depth} ---")

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

            print(f"\nKết quả:")
            print(f"  Minimax:      Điểm={score_min:.2f}, Nút={nodes_min}, Thời gian={time_min:.4f}s")
            print(f"  Alpha-Beta:   Điểm={score_ab:.2f}, Nút={nodes_ab}, Nhánh đã cắt={branches_ab}, Thời gian={time_ab:.4f}s")
            print(f"  Cải thiện:    Giảm nút {reduction_pct:.1f}%, Tiết kiệm thời gian {time_saving:.1f}%")

            # Xác minh điểm số có khớp nhau không (nên có với chơi hoàn hảo)
            if abs(score_min - score_ab) < 0.01:
                print(f"  ✓ Điểm số khớp")
            else:
                print(f"  ✗ Điểm số chênh lệch {abs(score_min - score_ab):.2f}")

    except Exception as e:
        print(f"Lỗi khi kiểm tra {team_name}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Khôi phục stats gốc của quân pieza
        formation.constants.PIECE_STATS = original_piece_stats

def main():
    print("So sánh Alpha-Beta Pruning vs Minimax")
    print("========================================")

    # Vì chúng ta chỉ có 5 loại quân, chúng ta sẽ kiểm tra với bộ đầy đủ
    # Nhưng chúng ta có thể chạy nhiều lần để xem hành vi trung bình

    all_pieces = ["Warrior", "Mage", "Archer", "Tank", "Assassin"]

    # Test 1: Trò chơi chuẩn với tất cả các loại quân
    test_formation_comparison("Trò chơi chuẩn (Tất cả 5 loại quân)", all_pieces)

    # Test 2: Chúng ta cũng có thể test với một hạt ngẫu nhiên để đa dạng
    import random
    print(f"\n{'='*60}")
    print("Đang chạy các test bổ sung với các hạt ngẫu nhiên")
    print(f"{'='*60}")

    for i in range(2):
        random.seed(42 + i)  # Fixed seed for reproducibility
        test_formation_comparison(f"Hạt ngẫu nhiên {42 + i}", all_pieces)

if __name__ == "__main__":
    main()