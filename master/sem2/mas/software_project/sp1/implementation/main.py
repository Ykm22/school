import asyncio
import logging
from utils.logger import setup_logger
from game.maze import Maze
from agents.pacman_agent import PacManAgent
from agents.environment_agent import EnvironmentAgent
from config.game_config import AGENT_JIDS, AGENT_PASSWORDS

async def main():
    # Setup logging
    logger = setup_logger()
    
    try:
        logger.info("Initializing Pac-Man Multi-Agent System...")
        
        # Create maze
        maze = Maze()
        logger.info("Maze created successfully")
        
        # Create agents
        pacman_agent = PacManAgent(
            AGENT_JIDS['pacman'],
            AGENT_PASSWORDS['pacman'],
            maze
        )
        
        environment_agent = EnvironmentAgent(
            AGENT_JIDS['environment'],
            AGENT_PASSWORDS['environment'],
            maze
        )
        
        logger.info("Agents created, starting system...")
        
        # Start agents with auto-registration
        await pacman_agent.start(auto_register=True)
        logger.info("Pac-Man agent started")
        
        await asyncio.sleep(1)  # Small delay between agent starts
        
        await environment_agent.start(auto_register=True)
        logger.info("Environment agent started")
        
        logger.info("All agents started successfully")
        
        # Wait for agents to run (check every second)
        while environment_agent.blackboard.get_game_state()['running']:
            await asyncio.sleep(1)
        
        logger.info("Game completed, stopping agents...")
        
        # Stop agents
        await pacman_agent.stop()
        await environment_agent.stop()
        
        logger.info("=== Pac-Man Multi-Agent System Ended ===")
    
    except Exception as e:
        logger.error(f"System error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
