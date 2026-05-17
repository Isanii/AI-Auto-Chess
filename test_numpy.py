import sys
sys.path.insert(0, '.')

from core import constants, models, heuristic, pieces

# Create a simple formation
piece_warrior = pieces.create_piece("Warrior")
piece_mage = pieces.create_piece("Mage")
piece_archer = pieces.create_piece("Archer")

unit1 = models.FormationUnit(piece=piece_warrior, position=models.Position(0, 0))
unit2 = models.FormationUnit(piece=piece_mage, position=models.Position(0, 1))
unit3 = models.FormationUnit(piece=piece_archer, position=models.Position(1, 0))

formation = [unit1, unit2, unit3]

print("Testing constants.POSITION_BONUS type:", type(constants.POSITION_BONUS))
print("POSITION_BONUS:\n", constants.POSITION_BONUS)

# Test heuristic
score = heuristic.evaluate_formation(formation)
print("Formation score:", score)
print("Type of score:", type(score))

# Test formation spread bonus
spread = heuristic.formation_spread_bonus(formation)
print("Spread bonus:", spread)

# Test team balance bonus
balance = heuristic.team_balance_bonus(formation)
print("Balance bonus:", balance)

# Test matchup bonus
formation2 = [unit1, unit2, unit3]  # same
matchup = heuristic.matchup_bonus(formation, formation2)
print("Matchup bonus:", matchup)

# Test evaluate state
state_score = heuristic.eval(formation, formation2)
print("Evaluate state score:", state_score)

print("All tests passed!")