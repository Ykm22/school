# import asyncio
# import logging
# from spade.behaviour import PeriodicBehaviour
# from utils.visualization import MazeVisualizer
# 
# logger = logging.getLogger('PacManMAS.EnvironmentBehavior')
# 
# class GameCoordinatorBehaviour(PeriodicBehaviour):
#     def __init__(self, agent):
#         super().__init__(period=0.2)  # 0.2 seconds coordination cycle
#         self.agent = agent
#         self.visualizer = MazeVisualizer(agent.maze)
#     
#     async def run(self):
#         game_state = self.agent.blackboard.get_game_state()
#         positions = self.agent.blackboard.get_all_positions()
#         
#         # Check power pellet status and update ghost modes
#         power_was_active = game_state.get('power_pellet_active', False)
#         self.agent.blackboard.check_power_pellet_status()
#         game_state = self.agent.blackboard.get_game_state()  # Get updated state
#         power_is_active = game_state.get('power_pellet_active', False)
#         
#         # Handle power pellet mode changes
#         if power_is_active and not power_was_active:
#             # Power pellet just activated - frighten ghosts
#             self._frighten_all_ghosts()
#         elif not power_is_active and power_was_active:
#             # Power pellet just expired - return ghosts to normal
#             self._normalize_all_ghosts()
#         
#         # Check for collisions
#         self._check_collisions(positions, game_state)
#         
#         logger.info(f"Environment coordinating step {game_state['step']}")
#         logger.debug(f"Current agent positions: {positions}")
#         
#         # Update visualization
#         self.visualizer.render(positions, game_state)
#         
#         # Check game completion or game over
#         if game_state.get('game_over', False):
#             logger.info("Game Over! PacMan was caught by a ghost!")
#             self.agent.blackboard.update_game_state('running', False)
#             return
#         
#         if game_state['game_complete'] or not game_state['running']:
#             logger.info("Game completed! Stopping environment agent...")
#             await self.agent.stop()
#             return
#         
#         # Check remaining collectibles
#         remaining = self.agent.maze.count_remaining_collectibles()
#         total_remaining = remaining['dots'] + remaining['power_pellets']
#         
#         if total_remaining == 0:
#             logger.info("All collectibles collected! Game completing...")
#             self.agent.blackboard.set_game_complete()
#     
#     def _frighten_all_ghosts(self):
#         """Set all ghosts to frightened mode"""
#         logger.info("Power pellet activated! All ghosts are now frightened!")
#         # Mark all ghosts as frightened in the blackboard
#         for ghost_name in ['blinky', 'pinky', 'inky', 'clyde']:
#             self.agent.blackboard.set_ghost_frightened(ghost_name)
# 
#     def _normalize_all_ghosts(self):
#         """Return all ghosts to normal mode"""
#         logger.info("Power pellet expired! Ghosts returning to normal mode!")
#         # Clear frightened status for all ghosts
#         for ghost_name in ['blinky', 'pinky', 'inky', 'clyde']:
#             self.agent.blackboard.clear_ghost_frightened(ghost_name)
#     
#     def _check_collisions(self, positions, game_state):
#         """Check for collisions between PacMan and ghosts"""
#         pacman_pos = positions.get('pacman')
#         if not pacman_pos:
#             return
#         
#         for agent_name, pos in positions.items():
#             if agent_name.startswith('ghost_') and pos == pacman_pos:
#                 ghost_name = agent_name.replace('ghost_', '')
#                 self._handle_collision(ghost_name, game_state)
#     
#     def _handle_collision(self, ghost_name, game_state):
#         """Handle collision between PacMan and a ghost"""
#         power_active = game_state.get('power_pellet_active', False)
#         
#         if power_active:
#             # PacMan eats the ghost
#             points = self.agent.blackboard.eat_ghost(ghost_name)
#             logger.info(f"PacMan ate ghost {ghost_name}! +{points} points!")
#             
#             # Reset ghost position
#             ghost_start_positions = {
#                 "blinky": (10, 9),
#                 "pinky": (9, 10),
#                 "inky": (10, 10),
#                 "clyde": (11, 10)
#             }
#             if ghost_name in ghost_start_positions:
#                 reset_pos = ghost_start_positions[ghost_name]
#                 self.agent.blackboard.update_agent_position(f"ghost_{ghost_name}", reset_pos)
#                 # Mark ghost as consumed in blackboard
#                 self.agent.blackboard.set_ghost_consumed(ghost_name)
#             
#         else:
#             # Ghost catches PacMan - Game Over
#             logger.info(f"Ghost {ghost_name} caught PacMan! Game Over!")
#             self.agent.blackboard.set_game_over()

# behaviors/environment_behaviors.py - Fixed collision detection

import asyncio
import logging
from spade.behaviour import PeriodicBehaviour
from utils.visualization import MazeVisualizer
from behaviors.messaging_behaviors import GameEventBroadcastBehaviour, StateQueryBehaviour
from communication.messages import PowerModeMessage

logger = logging.getLogger('PacManMAS.EnvironmentBehavior')

class GameCoordinatorBehaviour(PeriodicBehaviour, GameEventBroadcastBehaviour, StateQueryBehaviour):
    def __init__(self, agent):
        super().__init__(period=0.2)  # 0.2 seconds coordination cycle
        self.agent = agent
        self.visualizer = MazeVisualizer(agent.maze)
        self.last_power_state = False
        self.ghost_respawn_timers = {}
        self.power_pellet_timer = 0
    
    async def run(self):
        game_state = self.agent.get_cached_game_state()
        positions = self.agent.get_cached_all_positions()
        
        # Update power pellet timer
        if game_state.get('power_pellet_active', False):
            if self.power_pellet_timer > 0:
                self.power_pellet_timer -= 1
                if self.power_pellet_timer == 0:
                    # Power pellet expired
                    self.agent.coordinator.local_cache['game_state']['power_pellet_active'] = False
                    await self._normalize_all_ghosts()
        
        # Check power pellet status and update ghost modes
        power_was_active = self.last_power_state
        current_power_state = game_state.get('power_pellet_active', False)
        
        # Handle power pellet mode changes
        if current_power_state and not power_was_active:
            # Power pellet just activated - frighten ghosts
            self.power_pellet_timer = 40  # 8 seconds at 0.2s intervals
            await self._frighten_all_ghosts()
        
        self.last_power_state = current_power_state
        
        # Check for collisions
        await self._check_collisions(positions, game_state)
        
        # Update ghost respawn timers
        self._update_ghost_respawn_timers()
        
        logger.info(f"Environment coordinating step {game_state['step']}")
        logger.debug(f"Current agent positions: {positions}")
        
        # Update visualization
        self.visualizer.render(positions, game_state)
        
        # Check game completion or game over
        if game_state.get('game_over', False):
            logger.info("Game Over! PacMan was caught by a ghost!")
            self.agent.coordinator.local_cache['game_state']['running'] = False
            await self.agent.stop()
            return
        
        if game_state.get('game_complete', False) or not game_state.get('running', True):
            logger.info("Game completed! Stopping environment agent...")
            await self.agent.stop()
            return
        
        # Check remaining collectibles
        remaining = self.agent.maze.count_remaining_collectibles()
        total_remaining = remaining['dots'] + remaining['power_pellets']
        
        if total_remaining == 0:
            logger.info("All collectibles collected! Game completing...")
            await self.broadcast_game_event('game_complete')
            self.agent.coordinator.local_cache['game_state']['game_complete'] = True
    
    async def _frighten_all_ghosts(self):
        """Broadcast power pellet activation to all ghosts"""
        logger.info("Power pellet activated! Broadcasting to all ghosts!")
        
        power_msg = PowerModeMessage(
            self.agent.agent_name,
            active=True,
            duration=8.0
        )
        
        await self._broadcast_message(power_msg)
        
        # Mark all ghosts as frightened in our coordinator
        self.agent.coordinator.local_cache['frightened_ghosts'] = {'blinky', 'pinky', 'inky', 'clyde'}

    async def _normalize_all_ghosts(self):
        """Broadcast power pellet deactivation to all ghosts"""
        logger.info("Power pellet expired! Broadcasting to all ghosts!")
        
        power_msg = PowerModeMessage(
            self.agent.agent_name,
            active=False,
            duration=0
        )
        
        await self._broadcast_message(power_msg)
        
        # Clear frightened status in our coordinator
        self.agent.coordinator.local_cache['frightened_ghosts'].clear()
    
    async def _check_collisions(self, positions, game_state):
        """Check for collisions between PacMan and ghosts"""
        pacman_pos = positions.get('pacman')
        if not pacman_pos:
            return
        
        # Check each ghost position
        for ghost_name in ['blinky', 'pinky', 'inky', 'clyde']:
            ghost_key = f'ghost_{ghost_name}'
            ghost_pos = positions.get(ghost_key)
            
            if ghost_pos and ghost_pos == pacman_pos:
                # Check if ghost is in respawn (can't collide)
                if ghost_name not in self.ghost_respawn_timers:
                    await self._handle_collision(ghost_name, game_state)
    
    async def _handle_collision(self, ghost_name, game_state):
        """Handle collision between PacMan and a ghost"""
        power_active = game_state.get('power_pellet_active', False)
        
        if power_active:
            # PacMan eats the ghost
            ghosts_eaten = game_state.get('ghosts_eaten', 0)
            points = 200 * (2 ** ghosts_eaten)  # Increasing points: 200, 400, 800, 1600
            
            logger.info(f"PacMan ate ghost {ghost_name}! +{points} points!")
            
            # Update local game state
            self.agent.coordinator.local_cache['game_state']['ghosts_eaten'] += 1
            self.agent.coordinator.local_cache['game_state']['score'] += points
            
            # Get pacman position for the event
            positions = self.agent.get_cached_all_positions()
            pacman_pos = positions.get('pacman')
            
            # Broadcast ghost eaten event
            await self.broadcast_game_event(
                'ghost_eaten', 
                pacman_pos,
                points,
                extra_data={'ghost_name': ghost_name}
            )
            
            # Reset ghost position
            ghost_start_positions = {
                "blinky": (10, 9),
                "pinky": (9, 10),
                "inky": (10, 10),
                "clyde": (11, 10)
            }
            
            if ghost_name in ghost_start_positions:
                reset_pos = ghost_start_positions[ghost_name]
                # Update position in coordinator cache
                self.agent.coordinator.local_cache['agent_positions'][f'ghost_{ghost_name}'] = reset_pos
                # Mark ghost as consumed
                self.agent.coordinator.local_cache['consumed_ghosts'].add(ghost_name)
                # Set respawn timer
                self.ghost_respawn_timers[ghost_name] = 25  # 5 seconds at 0.2s intervals
            
        else:
            # Ghost catches PacMan - Game Over
            logger.info(f"Ghost {ghost_name} caught PacMan! Game Over!")
            self.agent.coordinator.local_cache['game_state']['game_over'] = True
            await self.broadcast_game_event('game_over')
    
    def _update_ghost_respawn_timers(self):
        """Update respawn timers for consumed ghosts"""
        expired_ghosts = []
        
        for ghost_name, timer in self.ghost_respawn_timers.items():
            if timer > 0:
                self.ghost_respawn_timers[ghost_name] = timer - 1
            else:
                # Ghost has respawned
                self.agent.coordinator.local_cache['consumed_ghosts'].discard(ghost_name)
                expired_ghosts.append(ghost_name)
        
        # Clean up expired timers
        for ghost_name in expired_ghosts:
            del self.ghost_respawn_timers[ghost_name]
            logger.info(f"Ghost {ghost_name} has respawned and returned to normal mode!")
    
    async def _broadcast_message(self, game_message):
        """Broadcast message to all known agents"""
        all_jids = [
            'pacman@localhost',
            'blinky@localhost',
            'pinky@localhost',
            'inky@localhost',
            'clyde@localhost'
        ]
        
        for jid in all_jids:
            if jid != str(self.agent.jid):
                from spade.message import Message
                msg = Message(to=jid)
                msg.body = game_message.to_json()
                await self.send(msg)
