# Memory: Added numpy for matrix calculations in combat system

**Description**: Updated the project to use numpy for POSITION_BONUS matrix as required by the assignment. Changed constants.py to use numpy array and added numpy to requirements.txt.

**Why**: The assignment required matrix calculations to be handled by numpy library.

**How to apply**: The POSITION_BONUS constant is now a numpy array. All existing code that accesses it with [row][col] continues to work unchanged. The rest of the system uses the same numerical values.