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
    'blinky': 'password',
    'pinky': 'password',
    'inky': 'password',
    'clyde': 'password'
}

# Agent JIDs (will be constructed with localhost)
AGENT_JIDS = {
    'pacman': 'pacman@localhost',
    'environment': 'environment@localhost',
    'blinky': 'blinky@localhost',
    'pinky': 'pinky@localhost',
    'inky': 'inky@localhost',
    'clyde': 'clyde@localhost'
}

# Directions
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

DIRECTION_NAMES = ['UP', 'DOWN', 'LEFT', 'RIGHT']

# Ghost configurations
GHOST_COLORS = {
    'blinky': 'Red',
    'pinky': 'Pink',
    'inky': 'Cyan',
    'clyde': 'Orange'
}

GHOST_PERSONALITIES = {
    'blinky': 'The Chaser - Directly pursues Pac-Man',
    'pinky': 'The Ambusher - Tries to get ahead of Pac-Man',
    'inky': 'The Flanker - Uses Blinky to create pincer movements',
    'clyde': 'The Alternator - Chases when far, retreats when close'
}
