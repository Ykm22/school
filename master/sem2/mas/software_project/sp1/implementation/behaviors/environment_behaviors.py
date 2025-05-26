import asyncio
import logging
from spade.behaviour import PeriodicBehaviour
from utils.visualization import MazeVisualizer

logger = logging.getLogger('PacManMAS.EnvironmentBehavior')

class GameCoordinatorBehaviour(PeriodicBehaviour):
    def __init__(self, agent):
        super().__init__(period=0.2)  # 0.2 seconds coordination cycle
        self.agent = agent
        self.visualizer = MazeVisualizer(agent.maze)
    
    async def run(self):
        game_state = self.agent.blackboard.get_game_state()
        positions = self.agent.blackboard.get_all_positions()
        
        # Check power pellet status and update ghost modes
        power_was_active = game_state.get('power_pellet_active', False)
        self.agent.blackboard.check_power_pellet_status()
        game_state = self.agent.blackboard.get_game_state()  # Get updated state
        power_is_active = game_state.get('power_pellet_active', False)
        
        # Handle power pellet mode changes
        if power_is_active and not power_was_active:
            # Power pellet just activated - frighten ghosts
            self._frighten_all_ghosts()
        elif not power_is_active and power_was_active:
            # Power pellet just expired - return ghosts to normal
            self._normalize_all_ghosts()
        
        # Check for collisions
        self._check_collisions(positions, game_state)
        
        logger.info(f"Environment coordinating step {game_state['step']}")
        logger.debug(f"Current agent positions: {positions}")
        
        # Update visualization
        self.visualizer.render(positions, game_state)
        
        # Check game completion or game over
        if game_state.get('game_over', False):
            logger.info("Game Over! PacMan was caught by a ghost!")
            self.agent.blackboard.update_game_state('running', False)
            return
        
        if game_state['game_complete'] or not game_state['running']:
            logger.info("Game completed! Stopping environment agent...")
            await self.agent.stop()
            return
        
        # Check remaining collectibles
        remaining = self.agent.maze.count_remaining_collectibles()
        total_remaining = remaining['dots'] + remaining['power_pellets']
        
        if total_remaining == 0:
            logger.info("All collectibles collected! Game completing...")
            self.agent.blackboard.set_game_complete()
    
    def _frighten_all_ghosts(self):
        """Set all ghosts to frightened mode"""
        logger.info("Power pellet activated! All ghosts are now frightened!")
        # Note: In a full implementation, you'd send messages to ghost agents
        # For now, ghosts will check power pellet status themselves
    
    def _normalize_all_ghosts(self):
        """Return all ghosts to normal mode"""
        logger.info("Power pellet expired! Ghosts returning to normal mode!")
    
    def _check_collisions(self, positions, game_state):
        """Check for collisions between PacMan and ghosts"""
        pacman_pos = positions.get('pacman')
        if not pacman_pos:
            return
        
        for agent_name, pos in positions.items():
            if agent_name.startswith('ghost_') and pos == pacman_pos:
                ghost_name = agent_name.replace('ghost_', '')
                self._handle_collision(ghost_name, game_state)
    
    def _handle_collision(self, ghost_name, game_state):
        """Handle collision between PacMan and a ghost"""
        power_active = game_state.get('power_pellet_active', False)
        
        if power_active:
            # PacMan eats the ghost
            points = self.agent.blackboard.eat_ghost(ghost_name)
            logger.info(f"PacMan ate ghost {ghost_name}! +{points} points!")
            
            # Reset ghost position (simulate consumption)
            # In a full implementation, send message to ghost agent to respawn
            
        else:
            # Ghost catches PacMan - Game Over
            logger.info(f"Ghost {ghost_name} caught PacMan! Game Over!")
            self.agent.blackboard.set_game_over()
