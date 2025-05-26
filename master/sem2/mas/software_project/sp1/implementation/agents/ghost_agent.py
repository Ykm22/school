import logging
from agents.base_agent import BaseGameAgent
from behaviors.ghost_behaviors import GhostBehaviour

logger = logging.getLogger('PacManMAS.GhostAgent')

class GhostAgent(BaseGameAgent):
    def __init__(self, jid, password, maze, ghost_name="blinky", start_position=None):
        super().__init__(jid, password, maze)
        self.ghost_name = ghost_name
        self.ghost_mode = "normal"  # normal, frightened, returning
        self.start_position = start_position or self._get_default_start_position()
        self.position = self.start_position
        self.respawn_timer = 0
        logger.info(f"Ghost agent {ghost_name} created at position {self.position}")
    
    def _get_default_start_position(self):
        # Default ghost starting position (center area)
        return (10, 9)
    
    async def setup(self):
        await super().setup()
        
        # Ensure ghost position is registered in blackboard
        self.blackboard.update_agent_position(f"ghost_{self.ghost_name}", self.position)
        
        # Add ghost behavior
        ghost_behaviour = GhostBehaviour(self)
        self.add_behaviour(ghost_behaviour)
        
        logger.info(f"Ghost agent {self.ghost_name} behaviors added and ready at position {self.position}")
    
    def set_mode(self, mode):
        """Set ghost mode: normal, frightened, returning"""
        if self.ghost_mode != mode:
            self.ghost_mode = mode
            self.blackboard.update_agent_position(f"ghost_{self.ghost_name}", self.position)
            logger.info(f"Ghost {self.ghost_name} mode changed to {mode}")
    
    def is_frightened(self):
        return self.ghost_mode == "frightened"
    
    def is_vulnerable(self):
        return self.ghost_mode == "frightened"
    
    def get_consumed(self):
        """Handle being consumed by PacMan"""
        self.ghost_mode = "returning"
        self.position = self.start_position
        self.blackboard.update_agent_position(f"ghost_{self.ghost_name}", self.position)
        logger.info(f"Ghost {self.ghost_name} consumed! Returning to start position")
        
        # After a short delay, return to normal mode
        self.respawn_timer = 5  # 5 steps to respawn
    
    def update_respawn(self):
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer == 0:
                self.ghost_mode = "normal"
                logger.info(f"Ghost {self.ghost_name} respawned and ready!")
