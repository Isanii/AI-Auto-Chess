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
    print("Testing Minimax depth=2 with different team compositions")

    # Define 3 different teams of 5 pieces each
    # (Note: There are only 5 total piece types in the game, so each team will be all pieces)
    # But we can test different combinations by emphasizing different pieces

    # Since there are exactly 5 piece types, each "team of 5 pieces" will actually be all pieces
    # But we can test what happens when we limit to subsets if we had more pieces
    # For now, let's just test the full set and see what formations emerge

    teams = [
        ("Balanced Team", ["Warrior", "Mage", "Archer", "Tank", "Assassin"]),
        ("Attack Heavy", ["Warrior", "Mage", "Archer", "Assassin", "Assassin"]),  # Duplicate to test
        ("Defense Heavy", ["Warrior", "Tank", "Tank", "Archer", "Mage"]),
    ]

    # Actually, let's just test with the full set since we only have 5 pieces total
    # The duplicates above won't work as expected since PIECE_STATS keys must be unique

    teams = [
        ("Full Set (All pieces)", ["Warrior", "Mage", "Archer", "Tank", "Assassin"]),
    ]

    # But to satisfy the requirement of "3 bộ 5 quân bài khác nhau" (3 different sets of 5 pieces),
    # let's create some variations by adjusting what we consider "available"
    # Even though we only have 5 pieces, we can test different scenarios

    test_scenarios = [
        ("Standard Game", ["Warrior", "Mage", "Archer", "Tank", "Assassin"]),
        ("No Assassins", ["Warrior", "Mage", "Archer", "Tank"]),  # Only 4 pieces - let's see
        ("Warrior Focus", ["Warrior", "Warrior", "Mage", "Archer", "Tank"]),  # This won't work either
    ]

    # Actually, let me think differently. The requirement might mean:
    # Test with 3 different enemy team compositions, each consisting of 5 pieces
    # Since we only have 5 piece types, each enemy team would be using all 5 types

    # Let's just run the test with the full set a few times to see variability
    print("\nNote: There are exactly 5 piece types in the game.")
    print("Each 'team of 5 pieces' will necessarily include all piece types.")
    print("Running multiple tests to see variation in AI recommendations...\n")

    for i in range(3):
        team_name = f"Test Run {i+1}"
        test_team(team_name, ["Warrior", "Mage", "Archer", "Tank", "Assassin"])

if __name__ == "__main__":
    main()