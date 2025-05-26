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
        
        # Create a fresh copy of the maze layout
        maze_copy = [list(row) for row in self.maze.layout]
        
        # First, clear any existing 'P' from the original layout
        # Replace original Pac-Man position with a dot
        start_x, start_y = self.maze.pacman_start
        if maze_copy[start_y][start_x] == 'P':
            maze_copy[start_y][start_x] = '.'
        
        # Now place agents on the maze
        for agent_name, pos in agents_positions.items():
            x, y = pos
            if 0 <= y < len(maze_copy) and 0 <= x < len(maze_copy[0]):
                if agent_name == 'pacman':
                    maze_copy[y][x] = 'P'
                # Add other agent types here when you implement ghosts
                # elif agent_name == 'blinky':
                #     maze_copy[y][x] = 'B'
        
        # Print the maze
        for row in maze_copy:
            print(''.join(row))
        
        print()
        print("Legend: # = Wall, . = Dot, P = Pac-Man")
        print("=" * 50)
        
        logger.info(f"Maze rendered with agents at: {agents_positions}")
