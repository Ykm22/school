import os
import logging

logger = logging.getLogger('PacManMAS.Visualization')

class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def render(self, agents_positions=None):
        self.clear_screen()
        
        if agents_positions is None:
            agents_positions = {}
        
        print("=" * 50)
        print("     PAC-MAN MULTI-AGENT SYSTEM")
        print("=" * 50)
        print()
        
        maze_copy = [list(row) for row in self.maze.layout]
        
        # Place agents on the maze
        for agent_name, pos in agents_positions.items():
            x, y = pos
            if agent_name == 'pacman':
                maze_copy[y][x] = 'P'
        
        # Print the maze
        for row in maze_copy:
            print(''.join(row))
        
        print()
        print("Legend: # = Wall, . = Dot, P = Pac-Man")
        print("=" * 50)
        
        logger.info(f"Maze rendered with agents at: {agents_positions}")
