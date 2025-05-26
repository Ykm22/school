import logging
from config.maze_layouts import MINI_MAZE
from config.game_config import DIRECTIONS

logger = logging.getLogger('PacManMAS.Maze')

class Maze:
    def __init__(self, layout=None):
        self.layout = layout if layout else MINI_MAZE
        self.width = len(self.layout[0])
        self.height = len(self.layout)
        self.pacman_start = self._find_pacman_start()
        logger.info(f"Maze initialized: {self.width}x{self.height}, Pac-Man start: {self.pacman_start}")
    
    def _find_pacman_start(self):
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == 'P':
                    return (x, y)
        return (9, 15)  # Default position if 'P' not found
    
    def is_wall(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.layout[y][x] == '#'
        return True  # Out of bounds is considered a wall
    
    def is_valid_position(self, x, y):
        return not self.is_wall(x, y)
    
    def get_valid_moves(self, x, y):
        valid_moves = []
        for direction, (dx, dy) in DIRECTIONS.items():
            new_x, new_y = x + dx, y + dy
            if self.is_valid_position(new_x, new_y):
                valid_moves.append(direction)
        logger.debug(f"Valid moves from ({x}, {y}): {valid_moves}")
        return valid_moves
    
    def get_cell(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.layout[y][x]
        return '#'  # Out of bounds
