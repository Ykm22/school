import asyncio
import random
import logging
from spade.behaviour import PeriodicBehaviour
from config.game_config import DIRECTIONS

logger = logging.getLogger('PacManMAS.PacManBehavior')

class RandomMoveBehaviour(PeriodicBehaviour):
    def __init__(self, agent):
        super().__init__(period=0.2)  # 0.2 seconds between moves
        self.agent = agent
    
    async def run(self):
        current_pos = self.agent.position
        x, y = current_pos
        
        logger.info(f"Pac-Man at position {current_pos}, planning next move...")
        
        # Check and collect item at current position first
        collected_item = self.agent.maze.collect_item(x, y)
        if collected_item == 'dot':
            self.agent.blackboard.collect_dot()
        elif collected_item == 'power_pellet':
            self.agent.blackboard.collect_power_pellet()
        
        # Check if game is complete
        if self.agent.maze.is_game_complete():
            logger.info("All collectibles gathered! Game complete!")
            self.agent.blackboard.set_game_complete()
            return
        
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
