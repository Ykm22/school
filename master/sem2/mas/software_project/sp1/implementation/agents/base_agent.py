# import logging
# from spade.agent import Agent
# from communication.blackboard import Blackboard
# 
# logger = logging.getLogger('PacManMAS.BaseAgent')
# 
# class BaseGameAgent(Agent):
#     def __init__(self, jid, password, maze):
#         super().__init__(jid, password)
#         self.maze = maze
#         self.blackboard = Blackboard()
#         self.position = (0, 0)
#         self.agent_name = jid.split('@')[0]
#         logger.info(f"Base agent {self.agent_name} initialized")
#     
#     async def setup(self):
#         logger.info(f"Agent {self.agent_name} setup started")
#         self.blackboard.update_agent_position(self.agent_name, self.position)
#         logger.info(f"Agent {self.agent_name} setup completed")

import logging
from spade.agent import Agent
from communication.distributed_coordinator import DistributedGameCoordinator
from behaviors.messaging_behaviors import MessageReceiveBehaviour, PositionBroadcastBehaviour

logger = logging.getLogger('PacManMAS.BaseAgent')

class BaseGameAgent(Agent):
    def __init__(self, jid, password, maze):
        super().__init__(jid, password)
        self.maze = maze
        self.position = (0, 0)
        self.agent_name = jid.split('@')[0]
        
        # Initialize distributed coordinator instead of blackboard
        self.coordinator = DistributedGameCoordinator(self.agent_name)
        
        logger.info(f"Base agent {self.agent_name} initialized with distributed coordinator")
    
    async def setup(self):
        logger.info(f"Agent {self.agent_name} setup started")
        
        # Add core messaging behaviors
        message_receiver = MessageReceiveBehaviour(self)
        self.add_behaviour(message_receiver)
        
        position_broadcaster = PositionBroadcastBehaviour(self)
        self.add_behaviour(position_broadcaster)
        
        # Update local position in coordinator
        self.coordinator.update_local_position(self.position)
        
        logger.info(f"Agent {self.agent_name} setup completed with messaging behaviors")
    
    def get_cached_agent_position(self, agent_name):
        """Get cached position of another agent"""
        return self.coordinator.get_agent_position(agent_name)
    
    def get_cached_all_positions(self):
        """Get all cached agent positions"""
        return self.coordinator.get_all_positions()
    
    def get_cached_game_state(self):
        """Get cached game state"""
        return self.coordinator.get_game_state()
    
    def update_position(self, new_position):
        """Update agent position and notify coordinator"""
        self.position = new_position
        self.coordinator.update_local_position(new_position)
