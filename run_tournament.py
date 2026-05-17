import sys
sys.path.insert(0, '.')

from core.tournament import run_tournament

def print_standings(strategies, standings, matrix):
    print("\n" + "="*60)
    print("TOURNAMENT RESULTS")
    print("="*60)

    # Print strategy names for reference
    print("\nStrategies:")
    for i, strategy in enumerate(strategies):
        print(f"  {i}: {strategy.name}")

    # Print win/loss/draw matrix
    print("\nMatch Results Matrix (Row vs Column):")
    print("     ", end="")
    for strategy in strategies:
        print(f"{strategy.name:>8}", end="")
    print()

    for i, strategy in enumerate(strategies):
        print(f"{strategy.name:>5}: ", end="")
        for j, result in enumerate(matrix[i]):
            print(f"{result:>8}", end="")
        print()

    # Calculate win rates and print standings
    print("\nStandings (sorted by win rate):")
    print("-"*60)
    print(f"{'Strategy':<15} {'W':<3} {'L':<3} {'D':<3} {'Win%':<6} {'Avg HP':<8} {'Avg Turns':<9}")
    print("-"*60)

    # Convert standings to list for sorting
    standings_list = []
    for name, stats in standings.items():
        total_games = stats["wins"] + stats["losses"] + stats["draws"]
        win_rate = (stats["wins"] / total_games * 100) if total_games > 0 else 0
        avg_hp = stats["remaining_hp"] / total_games if total_games > 0 else 0
        avg_turns = stats["total_turns"] / total_games if total_games > 0 else 0
        standings_list.append({
            "name": name,
            "wins": stats["wins"],
            "losses": stats["losses"],
            "draws": stats["draws"],
            "win_rate": win_rate,
            "avg_hp": avg_hp,
            "avg_turns": avg_turns
        })

    # Sort by win rate descending
    standings_list.sort(key=lambda x: x["win_rate"], reverse=True)

    for stats in standings_list:
        print(f"{stats['name']:<15} {stats['wins']:<3} {stats['losses']:<3} {stats['draws']:<3} "
              f"{stats['win_rate']:<6.1f} {stats['avg_hp']:<8.1f} {stats['avg_turns']:<9.1f}")

def main():
    print("Running tournament with 5 strategies...")
    print("Strategies: Random, Greedy-HP, Greedy-ATK, Minimax depth=2, Minimax depth=3")

    strategies, standings, matrix = run_tournament()
    print_standings(strategies, standings, matrix)

    print("\n" + "="*60)
    print("Tournament completed!")
    print("="*60)

if __name__ == "__main__":
    main()