# import asyncio
# import logging
# from utils.logger import setup_logger
# from game.maze import Maze
# from agents.pacman_agent import PacManAgent
# from agents.environment_agent import EnvironmentAgent
# from agents.ghost_agent import GhostAgent
# from config.game_config import AGENT_JIDS, AGENT_PASSWORDS
# 
# async def main():
#     # Setup logging
#     logger = setup_logger()
#     
#     try:
#         logger.info("Initializing Pac-Man Multi-Agent System...")
#         
#         # Create maze
#         maze = Maze()
#         logger.info("Maze created successfully")
#         
#         # Create agents
#         pacman_agent = PacManAgent(
#             AGENT_JIDS['pacman'],
#             AGENT_PASSWORDS['pacman'],
#             maze
#         )
#         
#         environment_agent = EnvironmentAgent(
#             AGENT_JIDS['environment'],
#             AGENT_PASSWORDS['environment'],
#             maze
#         )
#         
#         # Create all four ghost agents
#         blinky_agent = GhostAgent(
#             AGENT_JIDS['blinky'],
#             AGENT_PASSWORDS['blinky'],
#             maze,
#             ghost_name="blinky",
#             start_position=(10, 9)  # Starts outside ghost house
#         )
#         
#         pinky_agent = GhostAgent(
#             AGENT_JIDS['pinky'],
#             AGENT_PASSWORDS['pinky'],
#             maze,
#             ghost_name="pinky",
#             start_position=(9, 10)  # Starts inside ghost house
#         )
#         
#         inky_agent = GhostAgent(
#             AGENT_JIDS['inky'],
#             AGENT_PASSWORDS['inky'],
#             maze,
#             ghost_name="inky",
#             start_position=(10, 10)  # Starts inside ghost house
#         )
#         
#         clyde_agent = GhostAgent(
#             AGENT_JIDS['clyde'],
#             AGENT_PASSWORDS['clyde'],
#             maze,
#             ghost_name="clyde",
#             start_position=(11, 10)  # Starts inside ghost house
#         )
#         
#         logger.info("Agents created, starting system...")
#         
#         # Start agents with auto-registration
#         await pacman_agent.start(auto_register=True)
#         logger.info("Pac-Man agent started")
#         
#         await asyncio.sleep(0.5)  # Small delay between agent starts
#         
#         # Start all ghost agents
#         await blinky_agent.start(auto_register=True)
#         logger.info("Blinky ghost agent started")
#         await asyncio.sleep(0.5)
#         
#         await pinky_agent.start(auto_register=True)
#         logger.info("Pinky ghost agent started")
#         await asyncio.sleep(0.5)
#         
#         await inky_agent.start(auto_register=True)
#         logger.info("Inky ghost agent started")
#         await asyncio.sleep(0.5)
#         
#         await clyde_agent.start(auto_register=True)
#         logger.info("Clyde ghost agent started")
#         await asyncio.sleep(0.5)
#         
#         await environment_agent.start(auto_register=True)
#         logger.info("Environment agent started")
#         
#         logger.info("All agents started successfully")
#         
#         # Wait for game to run
#         while True:
#             game_state = environment_agent.blackboard.get_game_state()
#             if not game_state['running']:
#                 break
#             await asyncio.sleep(1)
#         
#         logger.info("Game ended, stopping agents...")
#         
#         # Stop agents
#         await pacman_agent.stop()
#         await blinky_agent.stop()
#         await pinky_agent.stop()
#         await inky_agent.stop()
#         await clyde_agent.stop()
#         await environment_agent.stop()
#         
#         # Show final results
#         final_state = environment_agent.blackboard.get_game_state()
#         if final_state.get('game_complete', False):
#             logger.info("🎉 GAME COMPLETED! 🎉")
#         elif final_state.get('game_over', False):
#             logger.info("💀 GAME OVER! 💀")
#         
#         logger.info(f"Final Score: {final_state.get('score', 0):,}")
#         logger.info("=== Pac-Man Multi-Agent System Ended ===")
#     
#     except Exception as e:
#         logger.error(f"System error: {e}")
#         raise
# 
# if __name__ == "__main__":
#     asyncio.run(main())


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
        logger.info("Initializing Pac-Man Multi-Agent System with XMPP Messaging...")
        
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
        
        # Create all four ghost agents
        blinky_agent = GhostAgent(
            AGENT_JIDS['blinky'],
            AGENT_PASSWORDS['blinky'],
            maze,
            ghost_name="blinky",
            start_position=(10, 9)  # Starts outside ghost house
        )
        
        pinky_agent = GhostAgent(
            AGENT_JIDS['pinky'],
            AGENT_PASSWORDS['pinky'],
            maze,
            ghost_name="pinky",
            start_position=(9, 10)  # Starts inside ghost house
        )
        
        inky_agent = GhostAgent(
            AGENT_JIDS['inky'],
            AGENT_PASSWORDS['inky'],
            maze,
            ghost_name="inky",
            start_position=(10, 10)  # Starts inside ghost house
        )
        
        clyde_agent = GhostAgent(
            AGENT_JIDS['clyde'],
            AGENT_PASSWORDS['clyde'],
            maze,
            ghost_name="clyde",
            start_position=(11, 10)  # Starts inside ghost house
        )
        
        logger.info("Agents created, starting distributed system...")
        
        # Start environment agent first (authoritative coordinator)
        await environment_agent.start(auto_register=True)
        logger.info("Environment agent started - now serving as game coordinator")
        await asyncio.sleep(1)  # Give environment time to initialize
        
        # Start Pac-Man agent
        await pacman_agent.start(auto_register=True)
        logger.info("Pac-Man agent started with distributed messaging")
        await asyncio.sleep(0.5)
        
        # Start all ghost agents
        await blinky_agent.start(auto_register=True)
        logger.info("Blinky ghost agent started with distributed messaging")
        await asyncio.sleep(0.5)
        
        await pinky_agent.start(auto_register=True)
        logger.info("Pinky ghost agent started with distributed messaging")
        await asyncio.sleep(0.5)
        
        await inky_agent.start(auto_register=True)
        logger.info("Inky ghost agent started with distributed messaging")
        await asyncio.sleep(0.5)
        
        await clyde_agent.start(auto_register=True)
        logger.info("Clyde ghost agent started with distributed messaging")
        await asyncio.sleep(0.5)
        
        logger.info("All agents started successfully with XMPP communication")
        logger.info("Game coordination now handled via distributed messaging")
        
        # Wait for game to run
        while True:
            game_state = environment_agent.get_cached_game_state()
            if not game_state['running']:
                break
            await asyncio.sleep(1)
        
        logger.info("Game ended, stopping agents...")
        
        # Stop agents
        await pacman_agent.stop()
        await blinky_agent.stop()
        await pinky_agent.stop()
        await inky_agent.stop()
        await clyde_agent.stop()
        await environment_agent.stop()
        
        # Show final results
        final_state = environment_agent.get_cached_game_state()
        if final_state.get('game_complete', False):
            logger.info("🎉 GAME COMPLETED! 🎉")
        elif final_state.get('game_over', False):
            logger.info("💀 GAME OVER! 💀")
        
        logger.info(f"Final Score: {final_state.get('score', 0):,}")
        logger.info("=== Pac-Man Distributed Multi-Agent System Ended ===")
    
    except Exception as e:
        logger.error(f"System error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
