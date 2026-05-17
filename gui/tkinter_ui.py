import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

from core import formation
from core import combat
from core import strategies
from core import minimax
from core import alphabeta
from core import counter_picker
from core import explanation
from core import constants

from gui.renderer import BoardRenderer


import csv
import matplotlib.pyplot as plt

from core import tournament

class AutoChessGUI:

    def __init__(self, root):
        self.current_log_index = 0
        
        self.current_result = None

        self.replay_running = False
        self.root = root
        self.replay_job = None
        self.tournament_matches = []

        self.current_match_index = 0

        self.tournament_standings = None

        self.replay_speed = 250

        self.paused = False
        self.root.title(
            "AI Auto-Chess Simulator"
        )

        self.root.state(
            "zoomed"
        )

        # MAIN FRAME
        self.main_frame = tk.Frame(
            self.root
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # LEFT
        self.canvas = tk.Canvas(
            self.main_frame,
            bg="#1E1E1E"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # RIGHT PANEL
        self.right_panel = tk.Frame(
            self.main_frame,
            width=360,
            bg="#2B2B2B"
        )

        self.right_panel.pack_propagate(False)

        self.right_panel.pack(
            side="right",
            fill="y"
        )

        self.renderer = BoardRenderer(
            self.canvas
        )
        self.stats_label = tk.Label(
            self.right_panel,
            text="AI Stats",
            justify="left",
            anchor="w",
            font=("Consolas", 10),
            fg="white",
            bg="#2B2B2B"
        )

        self.stats_label.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.setup_controls()

        self.player_team = None
        self.enemy_team = None

    def setup_controls(self):

        title = tk.Label(
            self.right_panel,
            text="AI AUTO-CHESS",
            font=("Arial", 18, "bold")
        )

        title.pack(
            pady=20
        )

        # STRATEGY A
        tk.Label(
            self.right_panel,
            text="Strategy A"
        ).pack()

        self.strategy_a = ttk.Combobox(
            self.right_panel,
            values=[
                "Random",
                "GreedyHP",
                "GreedyATK",
                "MinimaxDepth2",
                "MinimaxDepth3"
            ]
        )

        self.strategy_a.current(0)

        self.strategy_a.pack(
            pady=10
        )

        # STRATEGY B
        tk.Label(
            self.right_panel,
            text="Strategy B"
        ).pack()

        self.strategy_b = ttk.Combobox(
            self.right_panel,
            values=[
                "Random",
                "GreedyHP",
                "GreedyATK",
                "MinimaxDepth2",
                "MinimaxDepth3"
            ]
        )

        self.strategy_b.current(1)

        self.strategy_b.pack(
            pady=10
        )

        # BUTTON
        self.start_button = tk.Button(
            self.right_panel,
            text="START BATTLE",
            command=self.start_battle,
            height=2
        )

        self.start_button.pack(
            pady=20,
            fill="x",
            padx=20
        )

        self.counter_button = tk.Button(
            self.right_panel,
            text="COUNTER PICK",
            command=self.run_counter_pick,
            height=2
        )

        self.counter_button.pack(
            pady=10,
            fill="x",
            padx=20
        )

        self.tournament_button = tk.Button(
            self.right_panel,
            text="RUN TOURNAMENT",
            command=self.run_tournament,
            height=2
        )

        self.tournament_button.pack(
            pady=10,
            fill="x",
            padx=20
        )

        self.pause_button = tk.Button(
            self.right_panel,
            text="PAUSE",
            command=self.toggle_pause
        )

        self.pause_button.pack(
            pady=10,
            fill="x",
            padx=20
        )

        self.end_button = tk.Button(
            self.right_panel,
            text="END BATTLE",
            command=self.end_battle,
            height=2,
            bg="#ff6b6b",
            fg="white"
        )

        self.end_button.pack(
            pady=10,
            fill="x",
            padx=20
        )
        tk.Label(
            self.right_panel,
            text="Replay Speed"
        ).pack()

        self.speed_slider = tk.Scale(
            self.right_panel,
            from_=50,
            to=1000,
            orient="horizontal",
            command=self.update_speed
        )

        self.speed_slider.set(250)

        self.speed_slider.pack(
            fill="x",
            padx=20
        )
        # RESULT
        log_frame = tk.Frame(
            self.right_panel
        )

        log_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        scrollbar = tk.Scrollbar(
            log_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.result_text = tk.Text(
            log_frame,
            height=20,
            yscrollcommand=scrollbar.set,
            wrap="word"
        )

        self.result_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.result_text.yview
        )

        self.result_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def get_strategy_by_name(
        self,
        name
    ):

        mapping = {
            "Random":
                strategies.RandomStrategy(),

            "GreedyHP":
                strategies.GreedyHPStrategy(),

            "GreedyATK":
                strategies.GreedyATKStrategy(),

            "MinimaxDepth2":
                strategies.MinimaxDepth2Strategy(),

            "MinimaxDepth3":
                strategies.MinimaxDepth3Strategy()
        }

        return mapping[name]

    def start_battle(self):
        # STOP OLD REPLAY
        self.replay_running = False

        if self.replay_job:

            self.root.after_cancel(
                self.replay_job
            )

            self.replay_job = None
        self.result_text.delete(
            "1.0",
            "end"
        )

        strategy_a = self.get_strategy_by_name(
            self.strategy_a.get()
        )

        strategy_b = self.get_strategy_by_name(
            self.strategy_b.get()
        )

        formation_a = strategy_a.choose_formation()
        formation_b = strategy_b.choose_formation(
            formation_a
        )

        stats_text = (
            f"Minimax Nodes: {minimax.nodes_visited}\n"
            f"AlphaBeta Nodes: {alphabeta.nodes_visited}\n"
            f"Branches Pruned: {alphabeta.branches_pruned}"
        )

        self.stats_label.config(
            text=stats_text
        )

        # CREATE BATTLE TEAMS - strategy_a (Player) at bottom, strategy_b (Enemy) at top
        self.player_team = combat.create_battle_team(
            formation_a
        )

        self.enemy_team = combat.create_battle_team(
            formation_b
        )

        # DRAW
        self.renderer.draw_board()

        self.renderer.draw_team(
            self.player_team,
            "A"
        )

        self.renderer.draw_team(
            self.enemy_team,
            "B"
        )

        # SIMULATE
        self.current_result = combat.simulate_battle(
            formation_a,
            formation_b
        )
        self.current_log_index = 0

        self.replay_running = True
        self.start_button.config(
            state="disabled"
        )

        self.counter_button.config(
            state="disabled"
        )
        self.end_button.config(state="normal")
        self.replay_next_event()


    def replay_next_event(self):
        if self.paused:
            return
        if not self.replay_running:
            return

        if (
            self.current_log_index
            >=
            len(self.current_result.combat_log)
            ):

            self.replay_running = False

            self.start_button.config(
                state="normal"
            )

            self.counter_button.config(
                state="normal"
            )

            self.result_text.insert(
                "end",
                "\n=== BATTLE FINISHED ===\n"
            )

            self.result_text.insert(
                "end",
                f"Winner: "
                f"{self.current_result.winner}\n"
            )

            # Display winner on board
            if self.current_result.winner == "A":
                winner_text = "Player Wins!"
            elif self.current_result.winner == "B":
                winner_text = "Enemy Wins!"
            else:
                winner_text = "Draw!"

            self.renderer.draw_message(winner_text)
            self.replay_running = False
            self.end_button.config(state="disabled")
            return

        event = self.current_result.combat_log[
            self.current_log_index
        ]

        # UPDATE HP
        if event.defender_team == "A":

            target_team = self.player_team

        else:

            target_team = self.enemy_team

        for battle_unit in target_team:

            pos = battle_unit.unit.position

            if (
                pos.row == event.defender_row
                and
                pos.col == event.defender_col
            ):

                battle_unit.current_hp = (
                    event.defender_hp_after
                )

                if event.defender_dead:

                    battle_unit.alive = False

                break

        # REDRAW
        self.renderer.draw_board()

        self.renderer.draw_team(
            self.player_team,
            "A",

            highlight_pos=(
                event.attacker_row,
                event.attacker_col
            )
            if event.attacker_team == "A"
            else None
        )

        self.renderer.draw_team(
            self.enemy_team,
            "B",

            highlight_pos=(
                event.attacker_row,
                event.attacker_col
            )
            if event.attacker_team == "B"
            else None
        )
        self.renderer.draw_attack_line(
            event.attacker_row,
            event.attacker_col,
            event.defender_row,
            event.defender_col
        )
        self.renderer.draw_damage_popup(
            event.defender_row,
            event.defender_col,
            event.damage
        )
        # COMBAT LOG
        self.result_text.insert(
            "end",

            f"Turn {event.turn} | "
            f"{event.attacker_team} "
            f"{event.attacker_name}"
            f" attacked "
            f"{event.defender_team} "
            f"{event.defender_name}"
            f" | Damage={event.damage}"
            f" | HP="
            f"{event.defender_hp_before}"
            f"→"
            f"{event.defender_hp_after}\n"
        )

        self.result_text.see("end")

        self.current_log_index += 1

        # NEXT EVENT
        if self.replay_running:

            self.root.after(
                self.replay_speed,
                self.replay_next_event
            )

    def run_counter_pick(self):

        # STOP CURRENT REPLAY
        self.replay_running = False

        if self.replay_job:

            self.root.after_cancel(
                self.replay_job
            )

            self.replay_job = None

        # CLEAR LOG
        self.result_text.delete(
            "1.0",
            "end"
        )

        # GENERATE ENEMY FORMATION (placed at TOP)
        enemy_formation = formation.generate_random_formation(
            top_side=True  # Enemy at top (rows 0-1)
        )

        # FIND BEST COUNTER (placed at BOTTOM)
        counter_formation, score = (
            counter_picker.find_best_counter(
                enemy_formation
            )
        )

        # CREATE BATTLE TEAMS
        self.player_team = combat.create_battle_team(
            counter_formation  # Player gets the counter formation (bottom)
        )

        self.enemy_team = combat.create_battle_team(
            enemy_formation    # Enemy gets the random formation (top)
        )

        # DRAW BOARD
        self.renderer.draw_board()

        self.renderer.draw_team(
            self.player_team,
            "A"
        )

        self.renderer.draw_team(
            self.enemy_team,
            "B"
        )

        # HEADER
        self.result_text.insert(
            "end",
            "=== COUNTER PICK SIMULATION ===\n\n"
        )

        self.result_text.insert(
            "end",
            f"Heuristic Advantage: {score:.2f}\n\n"
        )

        # ENEMY TEAM
        self.result_text.insert(
            "end",
            "Enemy Team:\n"
        )

        for unit in enemy_formation:

            self.result_text.insert(
                "end",
                f"- {unit.piece.name}\n"
            )

        # COUNTER TEAM
        self.result_text.insert(
            "end",
            "\nCounter Team:\n"
        )

        for unit in counter_formation:

            self.result_text.insert(
                "end",
                f"- {unit.piece.name}\n"
            )

        # AI EXPLANATION
        self.result_text.insert(
            "end",
            "\nAI Explanation:\n"
        )

        reasons = explanation.explain_formation(
            counter_formation
        )

        for reason in reasons:

            self.result_text.insert(
                "end",
                f"{reason}\n"
            )

        # START SIMULATION
        self.result_text.insert(
            "end",
            "\n=== SIMULATION START ===\n\n"
        )

        # RUN BATTLE
        self.current_result = combat.simulate_battle(
            counter_formation,
            enemy_formation
        )

        self.current_log_index = 0

        self.replay_running = True

        self.replay_next_event()

    def run_tournament(self):

        self.replay_running = False

        # Clear previous tournament data
        if self.replay_job:
            self.root.after_cancel(self.replay_job)
            self.replay_job = None

        self.result_text.delete(
            "1.0",
            "end"
        )

        self.result_text.insert(
            "end",
            "=== RUNNING TOURNAMENT ===\n\n"
        )

        # Get all strategies
        all_strategies = strategies.get_all_strategies()

        # Initialize tournament data structures
        self.tournament_matches = []
        self.tournament_standings = {}
        self.current_match_index = 0

        # Initialize standings for each strategy
        for strategy in all_strategies:
            self.tournament_standings[strategy.name] = {
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "total_turns": 0
            }

        # Create all unique match pairs (avoid duplicates and self-matches)
        for i, strategy_a in enumerate(all_strategies):
            for j, strategy_b in enumerate(all_strategies):
                if i < j:  # Only unique pairs, avoid duplicates and self
                    self.tournament_matches.append((strategy_a, strategy_b))

        # Start the first match
        self.result_text.insert(
            "end",
            f"Total matches to play: {len(self.tournament_matches)}\n"
        )
        self.result_text.insert(
            "end",
            "Starting first match...\n\n"
        )

        # Begin tournament match replay
        self.run_next_tournament_match()

    def show_tournament_chart(
        self,
        standings
    ):

        names = [
            name
            for name, _ in standings
        ]

        wins = [
            stats["wins"]
            for _, stats in standings
        ]

        plt.figure(
            figsize=(8, 5)
        )

        plt.bar(
            names,
            wins
        )

        plt.title(
            "Tournament Wins"
        )

        plt.xlabel(
            "Strategies"
        )

        plt.ylabel(
            "Wins"
        )

        plt.tight_layout()

        plt.show()
    def run_next_tournament_match(self):

        if (
            self.current_match_index
            >=
            len(self.tournament_matches)
        ):

            self.show_final_tournament_results()
            return

        strategy_a, strategy_b = (
            self.tournament_matches[
                self.current_match_index
            ]
        )

        self.result_text.insert(
            "end",
            f"\n=== MATCH "
            f"{self.current_match_index + 1} ===\n"
        )

        self.result_text.insert(
            "end",
            f"{strategy_a.name}"
            f" vs "
            f"{strategy_b.name}\n\n"
        )

        # FORMATIONS
        formation_a = strategy_a.choose_formation()

        formation_b = strategy_b.choose_formation(
            formation_a
        )

        # CREATE TEAMS
        self.player_team = combat.create_battle_team(
            formation_a
        )

        self.enemy_team = combat.create_battle_team(
            formation_b
        )

        # DRAW
        self.renderer.draw_board()

        self.renderer.draw_team(
            self.player_team,
            "A"
        )

        self.renderer.draw_team(
            self.enemy_team,
            "B"
        )

        # SIMULATE
        self.current_result = combat.simulate_battle(
            formation_a,
            formation_b
        )

        self.current_log_index = 0

        self.replay_running = True

        self.current_strategy_a = strategy_a
        self.current_strategy_b = strategy_b

        self.replay_next_tournament_event()
    
    def replay_next_tournament_event(self):
        if self.paused:
            return
        if not self.replay_running:
            return

        if (
            self.current_log_index
            >=
            len(self.current_result.combat_log)
        ):

            winner = self.current_result.winner

            if winner == "A":

                self.tournament_standings[
                    self.current_strategy_a.name
                ]["wins"] += 1

                self.tournament_standings[
                    self.current_strategy_b.name
                ]["losses"] += 1

            elif winner == "B":

                self.tournament_standings[
                    self.current_strategy_b.name
                ]["wins"] += 1

                self.tournament_standings[
                    self.current_strategy_a.name
                ]["losses"] += 1

            else:

                self.tournament_standings[
                    self.current_strategy_a.name
                ]["draws"] += 1

                self.tournament_standings[
                    self.current_strategy_b.name
                ]["draws"] += 1

            self.result_text.insert(
                "end",
                f"Winner: {winner}\n"
            )

            # Display winner on board for tournament match
            if winner == "A":
                winner_text = f"{self.current_strategy_a.name} Wins!"
            elif winner == "B":
                winner_text = f"{self.current_strategy_b.name} Wins!"
            else:
                winner_text = "Draw!"

            self.renderer.draw_message(winner_text)

            self.current_match_index += 1

            self.root.after(
                1200,
                self.run_next_tournament_match
            )

            return

        event = self.current_result.combat_log[
            self.current_log_index
        ]

        # UPDATE HP
        if event.defender_team == "A":

            target_team = self.player_team

        else:

            target_team = self.enemy_team

        for battle_unit in target_team:

            pos = battle_unit.unit.position

            if (
                pos.row == event.defender_row
                and
                pos.col == event.defender_col
            ):

                battle_unit.current_hp = (
                    event.defender_hp_after
                )

                if event.defender_dead:

                    battle_unit.alive = False

                break

        # REDRAW
        self.renderer.draw_board()

        self.renderer.draw_team(
            self.player_team,
            "A",

            highlight_pos=(
                event.attacker_row,
                event.attacker_col
            )
            if event.attacker_team == "A"
            else None
        )

        self.renderer.draw_team(
            self.enemy_team,
            "B",

            highlight_pos=(
                event.attacker_row,
                event.attacker_col
            )
            if event.attacker_team == "B"
            else None
        )

        self.renderer.draw_attack_line(
            event.attacker_row,
            event.attacker_col,
            event.defender_row,
            event.defender_col
        )
        self.renderer.draw_damage_popup(
            event.defender_row,
            event.defender_col,
            event.damage
        )

        self.current_log_index += 1

        self.root.after(
            self.replay_speed,
            self.replay_next_tournament_event
        )
    def show_final_tournament_results(self):

        self.result_text.insert(
            "end",
            "\n=== FINAL STANDINGS ===\n\n"
        )

        sorted_standings = sorted(
            self.tournament_standings.items(),
            key=lambda x: x[1]["wins"],
            reverse=True
        )

        for rank, (name, stats) in enumerate(
            sorted_standings,
            start=1
        ):

            self.result_text.insert(
                "end",

                f"{rank}. "
                f"{name}"
                f" | W={stats['wins']}"
                f" L={stats['losses']}"
                f" D={stats['draws']}\n"
            )

        self.show_tournament_chart(
            sorted_standings
        )
    def update_speed(
        self,
        value
    ):

        self.replay_speed = int(value)

    def toggle_pause(self):

        self.paused = not self.paused

        if self.paused:

            self.pause_button.config(
                text="RESUME"
            )

        else:

            self.pause_button.config(
                text="PAUSE"
            )

            if self.replay_running:

                self.replay_next_event()

    def end_battle(self):
        """End the current battle/tournament replay"""
        self.replay_running = False
        self.paused = False

        # Cancel any pending replay jobs
        if self.replay_job:
            self.root.after_cancel(self.replay_job)
            self.replay_job = None

        # Reset button states
        self.start_button.config(state="normal")
        self.counter_button.config(state="normal")
        self.pause_button.config(text="PAUSE")
        self.end_button.config(state="disabled")

        # Clear units but keep board
        self.player_team = []
        self.enemy_team = []
        self.renderer.draw_board()

        # Redraw labels
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        board_pixel_size = (
            constants.BOARD_SIZE
            *
            constants.CELL_SIZE
        )

        offset_x = (
            canvas_width - board_pixel_size
        ) // 2

        offset_y = (
            canvas_height - board_pixel_size
        ) // 2

        # Draw Player and Enemy labels
        label_y_top = offset_y - 20
        label_y_bottom = offset_y + board_pixel_size + 20
        label_x = offset_x + board_pixel_size // 2

        self.canvas.create_text(
            label_x, label_y_top,
            text="Player",
            fill="white",
            font=("Arial", 16, "bold")
        )
        self.canvas.create_text(
            label_x, label_y_bottom,
            text="Enemy",
            fill="white",
            font=("Arial", 16, "bold")
        )

        # Clear any ongoing replay
        self.result_text.insert("end", "\n=== BATTLE ENDED ===\n")
    def export_tournament_results(
        self,
        standings
    ):

        with open(
            "tournament_results.csv",
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Strategy",
                    "Wins",
                    "Losses",
                    "Draws",
                    "AvgTurns"
                ]
            )

            for name, stats in standings:

                total_matches = (
                    stats["wins"]
                    +
                    stats["losses"]
                    +
                    stats["draws"]
                )

                avg_turns = (
                    stats["total_turns"]
                    /
                    max(1, total_matches)
                )

                writer.writerow(
                    [
                        name,
                        stats["wins"],
                        stats["losses"],
                        stats["draws"],
                        round(avg_turns, 2)
                    ]
                )
    def show_tournament_chart(
        self,
        standings
    ):

        names = [
            name
            for name, _ in standings
        ]

        wins = [
            stats["wins"]
            for _, stats in standings
        ]

        plt.figure(
            figsize=(8, 5)
        )

        plt.bar(
            names,
            wins
        )

        plt.title(
            "Tournament Wins"
        )

        plt.xlabel(
            "Strategies"
        )

        plt.ylabel(
            "Wins"
        )

        plt.tight_layout()

        plt.show()
def main():

    root = tk.Tk()

    app = AutoChessGUI(
        root
    )

    root.mainloop()