# Game configuration parameters

GAME_SPEED = 2.0  # Seconds between moves
MAZE_WIDTH = 19
MAZE_HEIGHT = 21

# Agent passwords for SPADE
AGENT_PASSWORDS = {
    'pacman': 'password',
    'environment': 'password'
}

# Agent JIDs (will be constructed with localhost)
AGENT_JIDS = {
    'pacman': 'pacman@localhost',
    'environment': 'environment@localhost'
}

# Directions
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

DIRECTION_NAMES = ['UP', 'DOWN', 'LEFT', 'RIGHT']
