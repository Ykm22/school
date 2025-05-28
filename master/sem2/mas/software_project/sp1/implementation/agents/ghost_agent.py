# import logging
# from agents.base_agent import BaseGameAgent
# from behaviors.ghost_behaviors import GhostBehaviour, BlinkyBehaviour, PinkyBehaviour, InkyBehaviour, ClydeBehaviour
# 
# logger = logging.getLogger('PacManMAS.GhostAgent')
# 
# class GhostAgent(BaseGameAgent):
#     def __init__(self, jid, password, maze, ghost_name="blinky", start_position=None):
#         super().__init__(jid, password, maze)
#         self.ghost_name = ghost_name
#         self.ghost_mode = "normal"  # normal, frightened, returning
#         self.start_position = start_position or self._get_default_start_position()
#         self.position = self.start_position
#         self.respawn_timer = 0
#         self.scatter_target = self._get_scatter_target()
#         logger.info(f"Ghost agent {ghost_name} created at position {self.position}")
#     
#     def _get_default_start_position(self):
#         """Get default starting positions for each ghost"""
#         positions = {
#             "blinky": (10, 9),    # Starts outside the ghost house
#             "pinky": (9, 10),     # Starts inside ghost house
#             "inky": (10, 10),     # Starts inside ghost house
#             "clyde": (11, 10)     # Starts inside ghost house
#         }
#         return positions.get(self.ghost_name, (10, 9))
#     
#     def _get_scatter_target(self):
#         """Get scatter mode target corners for each ghost"""
#         targets = {
#             "blinky": (19, 0),    # Top-right corner
#             "pinky": (0, 0),      # Top-left corner
#             "inky": (19, 20),     # Bottom-right corner
#             "clyde": (0, 20)      # Bottom-left corner
#         }
#         return targets.get(self.ghost_name, (10, 10))
#     
#     async def setup(self):
#         await super().setup()
#         
#         # Ensure ghost position is registered in blackboard
#         self.blackboard.update_agent_position(f"ghost_{self.ghost_name}", self.position)
#         
#         # Add ghost-specific behavior based on type
#         if self.ghost_name == "blinky":
#             ghost_behaviour = BlinkyBehaviour(self)
#         elif self.ghost_name == "pinky":
#             ghost_behaviour = PinkyBehaviour(self)
#         elif self.ghost_name == "inky":
#             ghost_behaviour = InkyBehaviour(self)
#         elif self.ghost_name == "clyde":
#             ghost_behaviour = ClydeBehaviour(self)
#         else:
#             ghost_behaviour = GhostBehaviour(self)  # Default behavior
#         
#         self.add_behaviour(ghost_behaviour)
#         
#         logger.info(f"Ghost agent {self.ghost_name} behaviors added and ready at position {self.position}")
#     
#     def set_mode(self, mode):
#         """Set ghost mode: normal, frightened, returning"""
#         if self.ghost_mode != mode:
#             self.ghost_mode = mode
#             self.blackboard.update_agent_position(f"ghost_{self.ghost_name}", self.position)
#             logger.info(f"Ghost {self.ghost_name} mode changed to {mode}")
#     
#     def is_frightened(self):
#         return self.ghost_mode == "frightened"
#     
#     def is_vulnerable(self):
#         return self.ghost_mode == "frightened"
#     
#     def get_consumed(self):
#         """Handle being consumed by PacMan"""
#         self.ghost_mode = "returning"
#         self.position = self.start_position
#         self.blackboard.update_agent_position(f"ghost_{self.ghost_name}", self.position)
#         logger.info(f"Ghost {self.ghost_name} consumed! Returning to start position")
#         
#         # After a short delay, return to normal mode
#         self.respawn_timer = 5  # 5 steps to respawn
#     
#     def update_respawn(self):
#         if self.respawn_timer > 0:
#             self.respawn_timer -= 1
#             if self.respawn_timer == 0:
#                 self.ghost_mode = "normal"
#                 logger.info(f"Ghost {self.ghost_name} respawned and ready!")

import logging
from agents.base_agent import BaseGameAgent
from behaviors.ghost_behaviors import GhostBehaviour, BlinkyBehaviour, PinkyBehaviour, InkyBehaviour, ClydeBehaviour

logger = logging.getLogger('PacManMAS.GhostAgent')

class GhostAgent(BaseGameAgent):
    def __init__(self, jid, password, maze, ghost_name="blinky", start_position=None):
        super().__init__(jid, password, maze)
        self.ghost_name = ghost_name
        self.ghost_mode = "normal"  # normal, frightened, returning
        self.start_position = start_position or self._get_default_start_position()
        self.position = self.start_position
        self.respawn_timer = 0
        self.scatter_target = self._get_scatter_target()
        logger.info(f"Ghost agent {ghost_name} created at position {self.position}")
    
    def _get_default_start_position(self):
        """Get default starting positions for each ghost"""
        positions = {
            "blinky": (10, 9),    # Starts outside the ghost house
            "pinky": (9, 10),     # Starts inside ghost house
            "inky": (10, 10),     # Starts inside ghost house
            "clyde": (11, 10)     # Starts inside ghost house
        }
        return positions.get(self.ghost_name, (10, 9))
    
    def _get_scatter_target(self):
        """Get scatter mode target corners for each ghost"""
        targets = {
            "blinky": (19, 0),    # Top-right corner
            "pinky": (0, 0),      # Top-left corner
            "inky": (19, 20),     # Bottom-right corner
            "clyde": (0, 20)      # Bottom-left corner
        }
        return targets.get(self.ghost_name, (10, 10))
    
    async def setup(self):
        await super().setup()
        
        # Ensure ghost position is registered in coordinator
        self.coordinator.update_local_position(self.position)
        
        # Add ghost-specific behavior based on type
        if self.ghost_name == "blinky":
            ghost_behaviour = BlinkyBehaviour(self)
        elif self.ghost_name == "pinky":
            ghost_behaviour = PinkyBehaviour(self)
        elif self.ghost_name == "inky":
            ghost_behaviour = InkyBehaviour(self)
        elif self.ghost_name == "clyde":
            ghost_behaviour = ClydeBehaviour(self)
        else:
            ghost_behaviour = GhostBehaviour(self)  # Default behavior
        
        self.add_behaviour(ghost_behaviour)
        
        logger.info(f"Ghost agent {self.ghost_name} behaviors added and ready at position {self.position}")
    
    def set_mode(self, mode):
        """Set ghost mode: normal, frightened, returning"""
        if self.ghost_mode != mode:
            self.ghost_mode = mode
            logger.info(f"Ghost {self.ghost_name} mode changed to {mode}")
    
    def is_frightened(self):
        return self.ghost_mode == "frightened"
    
    def is_vulnerable(self):
        return self.ghost_mode == "frightened"
    
    def get_consumed(self):
        """Handle being consumed by PacMan"""
        self.ghost_mode = "returning"
        self.position = self.start_position
        self.update_position(self.position)
        logger.info(f"Ghost {self.ghost_name} consumed! Returning to start position")
        
        # After a short delay, return to normal mode
        self.respawn_timer = 25  # 5 seconds at 0.2s intervals to respawn
    
    def update_respawn(self):
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer == 0:
                self.ghost_mode = "normal"
                logger.info(f"Ghost {self.ghost_name} respawned and ready!")
