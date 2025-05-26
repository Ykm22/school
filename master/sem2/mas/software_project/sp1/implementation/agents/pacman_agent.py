import logging
from agents.base_agent import BaseGameAgent
from behaviors.pacman_behaviors import RandomMoveBehaviour

logger = logging.getLogger('PacManMAS.PacManAgent')

class PacManAgent(BaseGameAgent):
    def __init__(self, jid, password, maze):
        super().__init__(jid, password, maze)
        self.position = maze.pacman_start
        logger.info(f"Pac-Man agent created at position {self.position}")
    
    async def setup(self):
        await super().setup()
        
        # Add random movement behavior
        random_move_behaviour = RandomMoveBehaviour(self)
        self.add_behaviour(random_move_behaviour)
        
        logger.info("Pac-Man agent behaviors added and ready")
