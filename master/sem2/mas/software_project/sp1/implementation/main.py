import asyncio
from utils.logger import setup_logger
from game import Maze
from agents import PacManAgent, EnvironmentAgent, GhostAgent
from config.game_config import AGENT_JIDS, AGENT_PASSWORDS, ACTIVE_GHOSTS

async def main():
    # Setup logging
    logger = setup_logger()
    
    try:
        logger.info("Initializing Pac-Man Multi-Agent System with XMPP Messaging...")
        
        # Create maze
        maze = Maze()
        logger.info("Maze created successfully")
        
        # Create PacMan and Environment agents
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
        
        # Create active ghost agents
        ghost_agents = []
        # Define default start positions for all possible ghosts
        ghost_start_positions = {
            "blinky": (10, 9),
            "pinky": (9, 10),
            "inky": (10, 10),
            "clyde": (11, 10)
        }

        logger.info(f"Attempting to create active ghosts: {ACTIVE_GHOSTS}")
        for ghost_name in ACTIVE_GHOSTS:
            if ghost_name in AGENT_JIDS and ghost_name in AGENT_PASSWORDS:
                start_pos = ghost_start_positions.get(ghost_name)
                if not start_pos: # Fallback if a ghost in ACTIVE_GHOSTS has no defined start_pos
                    logger.warning(f"No start position defined for active ghost '{ghost_name}', using GhostAgent default.")

                ghost_agent = GhostAgent(
                    AGENT_JIDS[ghost_name],
                    AGENT_PASSWORDS[ghost_name],
                    maze,
                    ghost_name=ghost_name,
                    start_position=start_pos
                )
                ghost_agents.append(ghost_agent)
                logger.info(f"Successfully created active ghost: {ghost_name}")
            else:
                logger.warning(f"Ghost '{ghost_name}' listed in ACTIVE_GHOSTS but missing JID/password. Skipping.")
                
        logger.info(f"Agents created ({len(ghost_agents) + 2} total), starting distributed system...")
        
        # Start ALL agents first, then wait for them to initialize
        logger.info("Starting all agents...")
        
        # Start environment agent
        await environment_agent.start(auto_register=True)
        
        # Start Pacman and active ghost agents in parallel
        agent_start_tasks = [pacman_agent.start(auto_register=True)]
        for GA in ghost_agents: # GA for Ghost Agent instance
            agent_start_tasks.append(GA.start(auto_register=True))
        
        await asyncio.gather(*agent_start_tasks)
        
        logger.info("All agents started, waiting for initialization...")
        await asyncio.sleep(3) # Give all agents time to initialize their behaviors
        
        logger.info("All agents initialized and ready with XMPP communication")
        logger.info("Game coordination now handled via distributed messaging")
        
        # Wait for game to run
        while True:
            game_state = environment_agent.get_cached_game_state()
            if not game_state.get('running', True): # Check if running is explicitly False
                break
            await asyncio.sleep(1)
            
        logger.info("Game ended, stopping agents...")
        
        # Stop agents
        agent_stop_tasks = [pacman_agent.stop(), environment_agent.stop()]
        for GA in ghost_agents:
            agent_stop_tasks.append(GA.stop())
            
        await asyncio.gather(*agent_stop_tasks)
        
        # Show final results
        final_state = environment_agent.get_cached_game_state()
        if final_state.get('game_complete', False):
            logger.info("🎉 GAME COMPLETED! 🎉")
        elif final_state.get('game_over', False):
            logger.info("💀 GAME OVER! 💀")
        
        logger.info(f"Final Score: {final_state.get('score', 0):,}")
        logger.info("=== Pac-Man Distributed Multi-Agent System Ended ===")
    
    except Exception as e:
        logger.error(f"System error: {e}", exc_info=True) # Added exc_info for better debugging
        raise

if __name__ == "__main__":
    asyncio.run(main())
