import asyncio
import random
import logging
from spade.behaviour import PeriodicBehaviour
from config.game_config import GAME_SPEED, DIRECTIONS

logger = logging.getLogger('PacManMAS.PacManBehavior')

class RandomMoveBehaviour(PeriodicBehaviour):
    def __init__(self, agent):
        super().__init__(period=GAME_SPEED)
        self.agent = agent
    
    async def run(self):
        current_pos = self.agent.position
        x, y = current_pos
        
        logger.info(f"Pac-Man at position {current_pos}, planning next move...")
        
        # Get valid moves
        valid_moves = self.agent.maze.get_valid_moves(x, y)
        
        if valid_moves:
            # Choose random valid move
            chosen_direction = random.choice(valid_moves)
            dx, dy = DIRECTIONS[chosen_direction]
            new_x, new_y = x + dx, y + dy
            
            # Update position
            self.agent.position = (new_x, new_y)
            self.agent.blackboard.update_agent_position(self.agent.agent_name, self.agent.position)
            
            logger.info(f"Pac-Man moved {chosen_direction} to position {self.agent.position}")
        else:
            logger.warning(f"Pac-Man has no valid moves from position {current_pos}")
        
        # Increment game step
        self.agent.blackboard.increment_step()
