# import logging
# from agents.base_agent import BaseGameAgent
# from behaviors.environment_behaviors import GameCoordinatorBehaviour
# 
# logger = logging.getLogger('PacManMAS.EnvironmentAgent')
# 
# class EnvironmentAgent(BaseGameAgent):
#     def __init__(self, jid, password, maze):
#         super().__init__(jid, password, maze)
#         logger.info("Environment agent created")
#     
#     async def setup(self):
#         await super().setup()
#         
#         # Add game coordination behavior
#         coordinator_behaviour = GameCoordinatorBehaviour(self)
#         self.add_behaviour(coordinator_behaviour)
#         
#         logger.info("Environment agent behaviors added and ready")

import logging
from agents.base_agent import BaseGameAgent
from behaviors.environment_behaviors import GameCoordinatorBehaviour

logger = logging.getLogger('PacManMAS.EnvironmentAgent')

class EnvironmentAgent(BaseGameAgent):
    def __init__(self, jid, password, maze):
        super().__init__(jid, password, maze)
        logger.info("Environment agent created - will serve as game coordinator")
    
    async def setup(self):
        await super().setup()
        
        # Add game coordination behavior
        coordinator_behaviour = GameCoordinatorBehaviour(self)
        self.add_behaviour(coordinator_behaviour)
        
        logger.info("Environment agent behaviors added and ready to coordinate game")
        
        # Initialize the environment as authoritative game state holder
        self.coordinator.local_cache['game_state']['running'] = True
        self.coordinator.local_cache['game_state']['step'] = 0
        self.coordinator.local_cache['game_state']['score'] = 0
        
        logger.info("Environment agent is now the authoritative game state coordinator")
