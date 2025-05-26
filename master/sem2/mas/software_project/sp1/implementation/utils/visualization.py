import os
import logging

logger = logging.getLogger('PacManMAS.Visualization')

class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def render(self, agents_positions=None, game_state=None):
        self.clear_screen()
        
        if agents_positions is None:
            agents_positions = {}
        if game_state is None:
            game_state = {}
        
        print("=" * 60)
        print("           PAC-MAN MULTI-AGENT SYSTEM")
        print("=" * 60)
        
        # Display game statistics
        score = game_state.get('score', 0)
        step = game_state.get('step', 0)
        dots_collected = game_state.get('dots_collected', 0)
        power_pellets_collected = game_state.get('power_pellets_collected', 0)
        power_active = game_state.get('power_pellet_active', False)
        
        print(f"Score: {score:,} | Step: {step} | Dots: {dots_collected} | Power Pellets: {power_pellets_collected}")
        
        if power_active:
            print("🌟 POWER PELLET ACTIVE! 🌟")
        
        print()
        
        # Create maze display using current maze state
        maze_copy = [list(row) for row in self.maze.maze_state]
        
        # Place agents on the maze
        for agent_name, pos in agents_positions.items():
            x, y = pos
            if 0 <= y < len(maze_copy) and 0 <= x < len(maze_copy[0]):
                if agent_name == 'pacman':
                    if power_active:
                        maze_copy[y][x] = '🅿'  # Powered-up Pac-Man
                    else:
                        maze_copy[y][x] = 'P'   # Normal Pac-Man
                elif agent_name.startswith('ghost_'):
                    ghost_name = agent_name.replace('ghost_', '')
                    if power_active:
                        maze_copy[y][x] = ghost_name.lower()[0]  # Lowercase for frightened (b, p, i, c)
                    else:
                        maze_copy[y][x] = ghost_name.upper()[0]  # Uppercase for normal (B, P, I, C)
        
        # Print the maze
        for row in maze_copy:
            print(''.join(row))
        
        print()
        
        # Calculate remaining collectibles
        remaining = self.maze.count_remaining_collectibles()
        remaining_total = remaining['dots'] + remaining['power_pellets']
        
        print(f"Remaining: {remaining['dots']} dots, {remaining['power_pellets']} power pellets ({remaining_total} total)")
        print("Legend: # = Wall, . = Dot, O = Power Pellet, P = Pac-Man")
        print("        B/b = Blinky (Red Ghost), P/p = Pinky, I/i = Inky, C/c = Clyde")
        print("        Uppercase = Normal, Lowercase = Frightened")
        
        if game_state.get('game_complete', False):
            print()
            print("🎉 CONGRATULATIONS! GAME COMPLETED! 🎉")
            print(f"Final Score: {score:,}")
        
        print("=" * 60)
        
        logger.debug(f"Maze rendered with agents at: {agents_positions}")
