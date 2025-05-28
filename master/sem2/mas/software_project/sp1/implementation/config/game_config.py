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

# All possible ghost types that the game logic knows about
ALL_GHOST_NAMES = [
    'blinky',
    'pinky',
    'inky',
    'clyde']

# USER CONFIGURABLE: Define which ghosts are active in the game
# Default to all ghosts being active. Modify this list to change participants.
# Example: ACTIVE_GHOSTS = ['blinky', 'pinky'] for only Blinky and Pinky
ACTIVE_GHOSTS = [
    'blinky',
    'pinky',
    'inky',
    'clyde'
]

# Helper function to get JIDs of all active game agents (Pacman, Environment, Active Ghosts)
def get_active_agent_jids():
    """Returns a list of JIDs for all currently active game agents."""
    jids = []
    if 'pacman' in AGENT_JIDS:
        jids.append(AGENT_JIDS['pacman'])
    if 'environment' in AGENT_JIDS:
        jids.append(AGENT_JIDS['environment'])
    
    for ghost_name in ACTIVE_GHOSTS:
        if ghost_name in AGENT_JIDS:
            jids.append(AGENT_JIDS[ghost_name])
        else:
            # This case should ideally not happen if ACTIVE_GHOSTS only contains valid names
            print(f"Warning: Ghost '{ghost_name}' is in ACTIVE_GHOSTS but has no JID defined.")
    return jids
