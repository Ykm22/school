# Game configuration parameters

GAME_SPEED = 0.2  # 0.2 seconds between moves (faster gameplay)
MAZE_WIDTH = 19
MAZE_HEIGHT = 21

# Scoring
SCORE_DOT = 10
SCORE_POWER_PELLET = 50
POWER_PELLET_DURATION = 8.0  # seconds

# Agent passwords for SPADE
AGENT_PASSWORDS = {
    'pacman': 'password',
    'environment': 'password',
    'blinky': 'password'
}

# Agent JIDs (will be constructed with localhost)
AGENT_JIDS = {
    'pacman': 'pacman@localhost',
    'environment': 'environment@localhost',
    'blinky': 'blinky@localhost'
}

# Directions
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

DIRECTION_NAMES = ['UP', 'DOWN', 'LEFT', 'RIGHT']
