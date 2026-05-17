import sys
import time
sys.path.insert(0, '.')

from core import formation, heuristic
from core import minimax
from core import alphabeta

def run_minimax(my_formation, opponent_formation, depth, maximizing=True):
    """Run minimax and return score, formation, nodes visited"""
    # Reset counter
    minimax.nodes_visited = 0
    start_time = time.time()
    score, best_formation = minimax.minimax(
        my_formation, opponent_formation, depth, maximizing
    )
    end_time = time.time()
    return score, best_formation, minimax.nodes_visited, end_time - start_time

def run_alphabeta(my_formation, opponent_formation, depth, maximizing=True):
    """Run alpha-beta and return score, formation, nodes visited, branches pruned"""
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
    """Test both algorithms with a specific team composition"""
    print(f"\n{'='*60}")
    print(f"Testing {team_name}")
    print(f"{'='*60}")

    # Backup original piece stats
    original_piece_stats = {}
    for k, v in formation.constants.PIECE_STATS.items():
        original_piece_stats[k] = v.copy()

    try:
        # Modify constants to only include these pieces
        formation.constants.PIECE_STATS = {
            k: v for k, v in original_piece_stats.items()
            if k in piece_names
        }

        # Create a fixed opponent formation for consistent testing
        # We'll use a preset formation rather than random for reproducibility
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

        print(f"Opponent formation (fixed):")
        for i, unit in enumerate(opponent_formation):
            print(f"  Unit {i+1}: {unit.piece.name} at ({unit.position.row}, {unit.position.col})")

        # Test depths 2 and 3
        for depth in [2, 3]:
            print(f"\n--- Depth {depth} ---")

            # Run Minimax
            print("Running Minimax...")
            score_min, form_min, nodes_min, time_min = run_minimax(
                None, opponent_formation, depth, maximizing=True
            )

            # Run Alpha-Beta
            print("Running Alpha-Beta...")
            score_ab, form_ab, nodes_ab, branches_ab, time_ab = run_alphabeta(
                None, opponent_formation, depth, maximizing=True
            )

            # Calculate savings
            if nodes_min > 0:
                reduction_pct = (1 - nodes_ab / nodes_min) * 100
            else:
                reduction_pct = 0

            time_saving = (1 - time_ab / time_min) * 100 if time_min > 0 else 0

            print(f"\nResults:")
            print(f"  Minimax:      Score={score_min:.2f}, Nodes={nodes_min}, Time={time_min:.4f}s")
            print(f"  Alpha-Beta:   Score={score_ab:.2f}, Nodes={nodes_ab}, Branches Pruned={branches_ab}, Time={time_ab:.4f}s")
            print(f"  Improvement:  Nodes reduced by {reduction_pct:.1f}%, Time saved by {time_saving:.1f}%")

            # Verify scores match (they should with perfect play)
            if abs(score_min - score_ab) < 0.01:
                print(f"  ✓ Scores match")
            else:
                print(f"  ✗ Scores differ by {abs(score_min - score_ab):.2f}")

    except Exception as e:
        print(f"Error testing {team_name}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Restore original piece stats
        formation.constants.PIECE_STATS = original_piece_stats

def main():
    print("Alpha-Beta Pruning vs Minimax Comparison")
    print("========================================")

    # Since we only have 5 piece types, we'll test with the full set
    # But we can run multiple iterations to see average behavior

    all_pieces = ["Warrior", "Mage", "Archer", "Tank", "Assassin"]

    # Test 1: Standard game with all pieces
    test_formation_comparison("Standard Game (All 5 pieces)", all_pieces)

    # Test 2: Let's also test with a random seed for variety
    import random
    print(f"\n{'='*60}")
    print("Running additional tests with random seeds")
    print(f"{'='*60}")

    for i in range(2):
        random.seed(42 + i)  # Fixed seed for reproducibility
        test_formation_comparison(f"Random Seed {42 + i}", all_pieces)

if __name__ == "__main__":
    main()