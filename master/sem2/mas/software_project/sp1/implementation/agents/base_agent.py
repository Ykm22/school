import logging
from spade.agent import Agent
from communication.blackboard import Blackboard

logger = logging.getLogger('PacManMAS.BaseAgent')

class BaseGameAgent(Agent):
    def __init__(self, jid, password, maze):
        super().__init__(jid, password)
        self.maze = maze
        self.blackboard = Blackboard()
        self.position = (0, 0)
        self.agent_name = jid.split('@')[0]
        logger.info(f"Base agent {self.agent_name} initialized")
    
    async def setup(self):
        logger.info(f"Agent {self.agent_name} setup started")
        self.blackboard.update_agent_position(self.agent_name, self.position)
        logger.info(f"Agent {self.agent_name} setup completed")
