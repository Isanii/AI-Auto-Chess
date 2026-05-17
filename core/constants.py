BOARD_SIZE = 4

TEAM_SIZE = 3

MAX_TURNS = 100

# GUI
CELL_SIZE = 140
BOARD_PADDING = 50

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

INFO_PANEL_WIDTH = 320


# Piece Stats
PIECE_STATS = {
    "Warrior": {
        "ATK": 3,
        "DEF": 5,
        "HP": 10
    },

    "Mage": {
        "ATK": 7,
        "DEF": 2,
        "HP": 6
    },

    "Archer": {
        "ATK": 5,
        "DEF": 3,
        "HP": 7
    },

    "Tank": {
        "ATK": 2,
        "DEF": 8,
        "HP": 15
    },

    "Assassin": {
        "ATK": 9,
        "DEF": 1,
        "HP": 5
    }
}


# Position bonus
POSITION_BONUS = [
    [0, 1, 1, 0],
    [1, 2, 2, 1],
    [1, 2, 2, 1],
    [0, 1, 1, 0]
]


# Heuristic weights
HP_WEIGHT = 1.0
ATK_WEIGHT = 1.5
DEF_WEIGHT = 1.2
CENTER_WEIGHT = 2.0


# Colors
WHITE = "#FFFFFF"
BLACK = "#000000"

GRAY = "#808080"
LIGHT_GRAY = "#DDDDDD"

GREEN = "#00AA00"
RED = "#CC3333"

TEAM_A_COLOR = "#4A90E2"
TEAM_B_COLOR = "#E94E77"

DARK_BG = "#1E1E1E"

DARK_PANEL = "#2B2B2B"

TEXT_COLOR = "#FFFFFF"


PIECE_COLORS = {
    "Warrior": "#3498DB",
    "Mage": "#9B59B6",
    "Archer": "#2ECC71",
    "Tank": "#F39C12",
    "Assassin": "#E74C3C"
}

# Positioning preferences

FRONTLINE_ROWS = [0, 1]

BACKLINE_ROWS = [2, 3]


ROLE_PREFERENCE = {

    "Tank": "front",

    "Warrior": "front",

    "Mage": "back",

    "Archer": "back",

    "Assassin": "back"
}
