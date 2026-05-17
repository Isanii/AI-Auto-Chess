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
        print("  {}: {}".format(i, strategy.name))

    # Print win/loss/draw matrix
    print("\nMatch Results Matrix (Row vs Column):")
    print("     ", end="")
    for strategy in strategies:
        print("{:>8}".format(strategy.name), end="")
    print()

    for i, strategy in enumerate(strategies):
        print("{:>5}: ".format(strategy.name), end="")
        for j, result in enumerate(matrix[i]):
            print("{:>8}".format(result), end="")
        print()

    # Calculate win rates and print standings
    print("\nStandings (sorted by win rate):")
    print("-"*60)
    print("{:<15} {:<3} {:<3} {:<3} {:<6} {:<8} {:<9}".format('Strategy', 'W', 'L', 'D', 'Win%', 'Avg HP', 'Avg Turns'))
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
        print("{:<15} {:<3} {:<3} {:<3} {:<6.1f} {:<8.1f} {:<9.1f}".format(
            stats['name'], stats['wins'], stats['losses'], stats['draws'],
            stats['win_rate'], stats['avg_hp'], stats['avg_turns']))

def main():
    print("Running tournament with 5 strategies...")
    print("Strategies: Random, Greedy-HP, Greedy-ATK, Minimax depth=2, Minimax depth=3")

    try:
        strategies, standings, matrix = run_tournament()
        print_standings(strategies, standings, matrix)

        print("\n" + "="*60)
        print("Tournament completed!")
        print("="*60)
    except Exception as e:
        print("Error running tournament: {}".format(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()