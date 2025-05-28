import asyncio
import logging
from spade.behaviour import PeriodicBehaviour
from utils.visualization import MazeVisualizer
from behaviors.messaging_behaviors import GameEventBroadcastBehaviour, StateQueryBehaviour
from communication.messages import PowerModeMessage
from config.game_config import ACTIVE_GHOSTS, get_active_agent_jids

logger = logging.getLogger('PacManMAS.EnvironmentBehavior')

class GameCoordinatorBehaviour(PeriodicBehaviour, GameEventBroadcastBehaviour, StateQueryBehaviour):
    def __init__(self, agent):
        super().__init__(period=0.2)  # 0.2 seconds coordination cycle
        self.agent = agent
        self.visualizer = MazeVisualizer(agent.maze)
        self.last_power_state = False
        self.ghost_respawn_timers = {}
        self.power_pellet_timer = 0
        self.previous_positions = {}
    
    async def run(self):
            # Fetch current authoritative game state and positions
            # This is the state *after* all agents have made their moves for the previous cycle
            # and broadcasted them.
            game_state_for_tick = self.agent.get_cached_game_state()
            current_positions_for_tick = self.agent.get_cached_all_positions()

            # --- Power Pellet Logic (example) ---
            # (Your existing power pellet activation/deactivation logic)
            # This might update game_state_for_tick or rely on broadcasts handled by the coordinator
            # For simplicity, ensure game_state_for_tick is fresh after this if it modifies power_pellet_active
            
            power_was_active = self.last_power_state
            current_power_state = game_state_for_tick.get('power_pellet_active', False)
            if current_power_state and not power_was_active:
                self.power_pellet_timer = 40 
                await self._frighten_all_ghosts()
            # (power pellet timer decrement and expiration logic...)
            self.last_power_state = current_power_state
            # --- End Power Pellet Logic ---

            # Perform collision checks using current and previous positions
            collision_resulted_in_game_over = await self._check_all_collisions(
                current_positions_for_tick,
                self.previous_positions, # Pass the positions from the *previous* completed tick
                game_state_for_tick      # Pass the game state relevant for this tick's collision rules
            )

            if collision_resulted_in_game_over:
                # Game is over, refresh state for final render and prepare to stop
                game_state_for_tick = self.agent.get_cached_game_state() 
                # No need to update self.previous_positions if game is ending
            else:
                # Update previous_positions for the *next* cycle if game continues
                self.previous_positions = current_positions_for_tick.copy()

            self._update_ghost_respawn_timers() # Manage ghost respawns

            # Logging and Visualization
            logger.info(f"Environment coordinating step {game_state_for_tick['step']}")
            # For render, use the most up-to-date positions after collision handling might have reset one
            render_positions = self.agent.get_cached_all_positions() 
            self.visualizer.render(render_positions, game_state_for_tick)

            # --- Game End Checks & Step Increment ---
            if game_state_for_tick.get('game_over', False) or \
            game_state_for_tick.get('game_complete', False) or \
            not game_state_for_tick.get('running', True):
                logger.info("Game ended! Stopping environment agent...")
                await self.agent.stop()
                return
            
            # (Check for game completion by collecting all items...)
            # (Increment step in environment's coordinator...)
            self.agent.coordinator.increment_step()

    async def _check_all_collisions(self, current_positions, previous_positions, game_state_rules):
        """
        Checks for direct and swap collisions between Pac-Man and Ghosts.
        Returns True if a game-ending collision (Pac-Man caught) occurs, False otherwise.
        Modifies the authoritative game state via self.agent.coordinator directly or via _handle_collision.
        """
        pacman_cur_pos = current_positions.get('pacman')
        pacman_prev_pos = previous_positions.get('pacman')

        if not pacman_cur_pos:
            return False # Pac-Man's current position is unknown

        for ghost_name in ['blinky', 'pinky', 'inky', 'clyde']:
            ghost_key = f'ghost_{ghost_name}'
            ghost_cur_pos = current_positions.get(ghost_key)
            ghost_prev_pos = previous_positions.get(ghost_key)

            if not ghost_cur_pos: # Ghost's current position is unknown
                continue

            # Skip collision if ghost is in respawn cooldown (tracked by EnvironmentBehaviour)
            if ghost_name in self.ghost_respawn_timers and self.ghost_respawn_timers[ghost_name] > 0:
                continue
            
            collision_occurred = False
            # 1. Direct Collision: Pac-Man and Ghost land on the same cell
            if pacman_cur_pos == ghost_cur_pos:
                logger.info(f"Direct collision detected: PacMan at {pacman_cur_pos}, {ghost_name} at {ghost_cur_pos}")
                collision_occurred = True
            # 2. Swap Collision: Pac-Man and Ghost swap cells
            elif pacman_prev_pos and ghost_prev_pos and \
                 pacman_cur_pos == ghost_prev_pos and ghost_cur_pos == pacman_prev_pos:
                logger.info(f"Swap collision detected: PacMan {pacman_prev_pos}->{pacman_cur_pos}, {ghost_name} {ghost_prev_pos}->{ghost_cur_pos}")
                collision_occurred = True

            if collision_occurred:
                # _handle_collision will determine if Pac-Man eats ghost or game over,
                # and will update the authoritative game state in self.agent.coordinator.
                await self._handle_collision(ghost_name, game_state_rules)
                
                # Check the authoritative game state *after* _handle_collision
                updated_game_state = self.agent.get_cached_game_state()
                if updated_game_state.get('game_over', False):
                    return True # Game-ending collision

                # If Pac-Man ate the ghost, the game continues, so we continue checking other ghosts.
        return False # No game-ending collision detected with any ghost
    
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
        for ghost_name in ACTIVE_GHOSTS:
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
        active_jids = get_active_agent_jids()
        
        for jid in active_jids:
            if jid != str(self.agent.jid):
                from spade.message import Message
                msg = Message(to=jid)
                msg.body = game_message.to_json()
                await self.send(msg)
