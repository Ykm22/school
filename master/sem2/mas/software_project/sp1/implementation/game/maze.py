import logging
from config.maze_layouts import MINI_MAZE
from config.game_config import DIRECTIONS

logger = logging.getLogger('PacManMAS.Maze')

class Maze:
    def __init__(self, layout=None):
        self.layout = layout if layout else MINI_MAZE
        self.width = len(self.layout[0])
        self.height = len(self.layout)
        
        # Create mutable maze state
        self.maze_state = [list(row) for row in self.layout]
        
        self.pacman_start = self._find_pacman_start()
        
        # Replace initial 'P' with dot
        start_x, start_y = self.pacman_start
        if self.maze_state[start_y][start_x] == 'P':
            self.maze_state[start_y][start_x] = '.'
        
        # Count initial dots and power pellets
        self.initial_dots = self._count_collectibles()
        
        logger.info(f"Maze initialized: {self.width}x{self.height}, Pac-Man start: {self.pacman_start}")
        logger.info(f"Total collectibles: {self.initial_dots['dots']} dots, {self.initial_dots['power_pellets']} power pellets")
    
    def _find_pacman_start(self):
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == 'P':
                    return (x, y)
        return (9, 15)
    
    def _count_collectibles(self):
        dots = 0
        power_pellets = 0
        for row in self.maze_state:
            for cell in row:
                if cell == '.':
                    dots += 1
                elif cell == 'O':
                    power_pellets += 1
        return {'dots': dots, 'power_pellets': power_pellets}
    
    def is_wall(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.maze_state[y][x] == '#'
        return True
    
    def is_valid_position(self, x, y):
        return not self.is_wall(x, y)
    
    def get_valid_moves(self, x, y):
        valid_moves = []
        for direction, (dx, dy) in DIRECTIONS.items():
            new_x, new_y = x + dx, y + dy
            if self.is_valid_position(new_x, new_y):
                valid_moves.append(direction)
        return valid_moves
    
    def get_cell(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.maze_state[y][x]
        return '#'
    
    def collect_item(self, x, y):
        """Collect item at position and return what was collected"""
        if 0 <= y < self.height and 0 <= x < self.width:
            cell = self.maze_state[y][x]
            if cell == '.':
                self.maze_state[y][x] = ' '  # Replace with empty space
                logger.info(f"Dot collected at ({x}, {y})")
                return 'dot'
            elif cell == 'O':
                self.maze_state[y][x] = ' '  # Replace with empty space
                logger.info(f"Power pellet collected at ({x}, {y})")
                return 'power_pellet'
        return None
    
    def count_remaining_collectibles(self):
        """Count remaining dots and power pellets"""
        return self._count_collectibles()
    
    def is_game_complete(self):
        """Check if all collectibles have been collected"""
        remaining = self.count_remaining_collectibles()
        total_remaining = remaining['dots'] + remaining['power_pellets']
        return total_remaining == 0
