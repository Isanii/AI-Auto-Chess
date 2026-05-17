import sys
import time
sys.path.insert(0, '.')

from core import formation, heuristic, pieces, models
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

def print_formation(formation, label):
    print(label + ":")
    for i, unit in enumerate(formation):
        print("  {}. {} at ({}, {})".format(i+1, unit.piece.name, unit.position.row, unit.position.col))
    print()

def main():
    print("Alpha-Beta Pruning vs Minimax Comparison")
    print("=" * 50)

    # Use a fixed opponent formation for consistent testing
    opponent_formation = [
        models.FormationUnit(piece=pieces.create_piece("Tank"), position=models.Position(3, 0)),
        models.FormationUnit(piece=pieces.create_piece("Mage"), position=models.Position(2, 1)),
        models.FormationUnit(piece=pieces.create_piece("Assassin"), position=models.Position(2, 2))
    ]

    print("Opponent formation:")
    print_formation(opponent_formation, "Opponent (Top Side)")

    # Test depths 2 and 3
    for depth in [2, 3]:
        print("\n--- Depth {} ---".format(depth))

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

        print("\nResults:")
        print("  Minimax:      Score={:.2f}, Nodes={}, Time={:.4f}s".format(score_min, nodes_min, time_min))
        print("  Alpha-Beta:   Score={:.2f}, Nodes={}, Branches Pruned={}, Time={:.4f}s".format(score_ab, nodes_ab, branches_ab, time_ab))
        print("  Improvement:  Nodes reduced by {:.1f}%, Time saved by {:.1f}%".format(reduction_pct, time_saving))

        # Verify scores match (they should with perfect play)
        if abs(score_min - score_ab) < 0.01:
            print("  Scores match")
        else:
            print("  Scores differ by {:.2f}".format(abs(score_min - score_ab)))

        # Show AI formations
        print("\n  Minimax AI formation:")
        print_formation(form_min, "")

        print("  Alpha-Beta AI formation:")
        print_formation(form_ab, "")

if __name__ == "__main__":
    main()