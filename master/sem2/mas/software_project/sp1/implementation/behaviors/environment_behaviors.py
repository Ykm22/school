import asyncio
import logging
from spade.behaviour import PeriodicBehaviour
from config.game_config import GAME_SPEED
from utils.visualization import MazeVisualizer

logger = logging.getLogger('PacManMAS.EnvironmentBehavior')

class GameCoordinatorBehaviour(PeriodicBehaviour):
    def __init__(self, agent):
        super().__init__(period=GAME_SPEED)
        self.agent = agent
        self.visualizer = MazeVisualizer(agent.maze)
    
    async def run(self):
        game_state = self.agent.blackboard.get_game_state()
        positions = self.agent.blackboard.get_all_positions()
        
        logger.info(f"Environment coordinating step {game_state['step']}")
        logger.info(f"Current agent positions: {positions}")
        
        # Update visualization
        self.visualizer.render(positions)
        
        # Check game state
        if game_state['step'] >= 5:  # Stop after 5 steps for this demo
            logger.info("Demo completed after 5 steps")
            self.agent.blackboard.update_game_state('running', False)
            await self.agent.stop()
