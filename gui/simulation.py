from core import combat


class BattleSimulation:

    def __init__(
        self,
        formation_a,
        formation_b
    ):

        self.result = combat.simulate_battle(
            formation_a,
            formation_b
        )

        self.current_index = 0

    def has_next(self):

        return (
            self.current_index
            <
            len(self.result.combat_log)
        )

    def next_event(self):

        if not self.has_next():
            return None

        event = self.result.combat_log[
            self.current_index
        ]

        self.current_index += 1

        return event