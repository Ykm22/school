import asyncio
import logging
from utils.logger import setup_logger
from game.maze import Maze
from agents.pacman_agent import PacManAgent
from agents.environment_agent import EnvironmentAgent
from agents.ghost_agent import GhostAgent
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
        
        # Create ghost agent
        ghost_agent = GhostAgent(
            AGENT_JIDS['blinky'],
            AGENT_PASSWORDS['blinky'],
            maze,
            ghost_name="blinky",
            start_position=(10, 9)  # Start near center
        )
        
        logger.info("Agents created, starting system...")
        
        # Start agents with auto-registration
        await pacman_agent.start(auto_register=True)
        logger.info("Pac-Man agent started")
        
        await asyncio.sleep(1)  # Small delay between agent starts
        
        await ghost_agent.start(auto_register=True)
        logger.info("Ghost agent started")
        
        await asyncio.sleep(1)
        
        await environment_agent.start(auto_register=True)
        logger.info("Environment agent started")
        
        logger.info("All agents started successfully")
        
        # Wait for game to run
        while True:
            game_state = environment_agent.blackboard.get_game_state()
            if not game_state['running']:
                break
            await asyncio.sleep(1)
        
        logger.info("Game ended, stopping agents...")
        
        # Stop agents
        await pacman_agent.stop()
        await ghost_agent.stop()
        await environment_agent.stop()
        
        # Show final results
        final_state = environment_agent.blackboard.get_game_state()
        if final_state.get('game_complete', False):
            logger.info("🎉 GAME COMPLETED! 🎉")
        elif final_state.get('game_over', False):
            logger.info("💀 GAME OVER! 💀")
        
        logger.info(f"Final Score: {final_state.get('score', 0):,}")
        logger.info("=== Pac-Man Multi-Agent System Ended ===")
    
    except Exception as e:
        logger.error(f"System error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
