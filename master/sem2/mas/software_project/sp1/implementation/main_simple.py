import asyncio
import random
import logging
from utils.logger import setup_logger
from game import Maze
from communication.distributed_coordinator import DistributedGameCoordinator
from utils.visualization import MazeVisualizer
from config.game_config import DIRECTIONS

class SimplePacManAgent:
    def __init__(self, maze):
        self.maze = maze
        self.position = maze.pacman_start
        self.coordinator = DistributedGameCoordinator('pacman')
        self.logger = logging.getLogger('PacManMAS.SimplePacMan')
        
    async def make_move(self):
        x, y = self.position
        self.logger.info(f"Pac-Man at position {self.position}, planning next move...")
        
        # Get valid moves
        valid_moves = self.maze.get_valid_moves(x, y)
        
        if valid_moves:
            # Choose random valid move
            chosen_direction = random.choice(valid_moves)
            dx, dy = DIRECTIONS[chosen_direction]
            new_x, new_y = x + dx, y + dy
            
            # Update position
            self.position = (new_x, new_y)
            self.coordinator.update_local_position(self.position)
            
            self.logger.info(f"Pac-Man moved {chosen_direction} to position {self.position}")
        else:
            self.logger.warning(f"Pac-Man has no valid moves from position {self.position}")

class SimpleEnvironmentAgent:
    def __init__(self, maze):
        self.maze = maze
        self.coordinator = DistributedGameCoordinator('environment')
        self.visualizer = MazeVisualizer(maze)
        self.logger = logging.getLogger('PacManMAS.SimpleEnvironment')
        
    async def coordinate_step(self, step):
        positions = self.coordinator.get_all_positions()
        
        self.logger.info(f"Environment coordinating step {step}")
        self.logger.info(f"Current agent positions: {positions}")
        
        # Update visualization
        game_state = self.coordinator.get_game_state()
        self.visualizer.render(positions, game_state)

async def main():
    # Setup logging
    logger = setup_logger()
    
    try:
        logger.info("Initializing Simple Pac-Man Distributed Multi-Agent System...")
        
        # Create maze
        maze = Maze()
        logger.info("Maze created successfully")
        
        # Create simple agents with distributed coordinators
        pacman = SimplePacManAgent(maze)
        environment = SimpleEnvironmentAgent(maze)
        
        # Initialize both coordinators with starting position
        pacman.coordinator.update_local_position(pacman.position)
        environment.coordinator.update_local_position(pacman.position)  # Environment knows about PacMan
        
        logger.info("Simple agents created with distributed coordination, starting simulation...")
        
        # Run simulation for 5 steps
        for step in range(1, 6):
            logger.info(f"=== STEP {step} ===")
            
            # Environment coordinates and displays current state
            await environment.coordinate_step(step)
            
            # Wait a moment to see the display
            await asyncio.sleep(1)
            
            # Pac-Man makes a move
            await pacman.make_move()
            
            # Increment step in both coordinators
            pacman.coordinator.increment_step()
            environment.coordinator.increment_step()
            
            # Simulate position sharing (in real XMPP version this would be automatic)
            environment.coordinator.local_cache['agent_positions']['pacman'] = pacman.position
            
            # Wait between steps
            await asyncio.sleep(2)
        
        logger.info("=== SIMULATION COMPLETED ===")
        logger.info("Final display:")
        await environment.coordinate_step("FINAL")
        
        logger.info("=== Simple Pac-Man Distributed Multi-Agent System Ended ===")
    
    except Exception as e:
        logger.error(f"System error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
