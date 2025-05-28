import logging
from agents.base_agent import BaseGameAgent
from behaviors.pacman_behaviors import SmartPacManBehaviour

logger = logging.getLogger('PacManMAS.PacManAgent')

class PacManAgent(BaseGameAgent):
    def __init__(self, jid, password, maze, use_smart_ai=True):
        super().__init__(jid, password, maze)
        self.position = maze.pacman_start
        self.use_smart_ai = use_smart_ai
        logger.info(f"Pac-Man agent created at position {self.position} (Smart AI: {use_smart_ai})")
    
    async def setup(self):
        await super().setup()
        
        # Set initial position in coordinator
        self.coordinator.update_local_position(self.position)
        
        # Add appropriate movement behavior
        if self.use_smart_ai or True: # hehe
            move_behaviour = SmartPacManBehaviour(self)
            logger.info("Pac-Man using SMART AI behavior with XMPP messaging")
        
        self.add_behaviour(move_behaviour)
        
        logger.info("Pac-Man agent behaviors added and ready for distributed gameplay")
