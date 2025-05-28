# import asyncio
# import random
# import logging
# from spade.behaviour import PeriodicBehaviour
# from config.game_config import DIRECTIONS
# 
# logger = logging.getLogger('PacManMAS.GhostBehavior')
# 
# class GhostBehaviour(PeriodicBehaviour):
#     """Base ghost behavior class"""
#     def __init__(self, agent):
#         super().__init__(period=0.2)  # Same speed as PacMan
#         self.agent = agent
#         self.last_position = None  # Track last position to avoid getting stuck
#         self.mode_timer = 0
#         self.scatter_duration = 70  # 7 seconds in scatter mode
#         self.chase_duration = 200   # 20 seconds in chase mode
#         self.current_phase = "scatter"  # Start in scatter mode
#     
#     async def run(self):
#         # Update respawn timer
#         self.agent.update_respawn()
#         
#         # Check if ghost was consumed and needs to reset
#         if self.agent.blackboard.is_ghost_consumed(self.agent.ghost_name):
#             self.agent.position = self.agent.start_position
#             self.agent.ghost_mode = "returning"
#             self.agent.respawn_timer = 5
#             self.agent.blackboard.clear_ghost_consumed(self.agent.ghost_name)
#             logger.info(f"Ghost {self.agent.ghost_name} resetting position after being consumed")
# 
#         if self.agent.blackboard.is_ghost_frightened(self.agent.ghost_name):
#             if self.agent.ghost_mode != "frightened" and self.agent.ghost_mode != "returning":
#                 self.agent.set_mode("frightened")
#                 self.agent.blackboard.clear_ghost_frightened(self.agent.ghost_name) 
# 
#         current_pos = self.agent.position
#         
#         # Get PacMan's position for AI decisions
#         pacman_pos = self.agent.blackboard.get_agent_position('pacman')
#         
#         logger.info(f"Ghost {self.agent.ghost_name} at {current_pos}, mode: {self.agent.ghost_mode}")
#         
#         # Check if power pellet is active to determine mode
#         game_state = self.agent.blackboard.get_game_state()
#         power_active = game_state.get('power_pellet_active', False)
#         
#         if power_active and self.agent.ghost_mode != "returning":
#             if self.agent.ghost_mode != "frightened":
#                 self.agent.set_mode("frightened")
#         else:
#             if self.agent.ghost_mode == "frightened":
#                 self.agent.set_mode("normal")
#         
#         # Update scatter/chase phase timer (only in normal mode)
#         if self.agent.ghost_mode == "normal":
#             self.mode_timer += 1
#             if self.current_phase == "scatter" and self.mode_timer >= self.scatter_duration:
#                 self.current_phase = "chase"
#                 self.mode_timer = 0
#             elif self.current_phase == "chase" and self.mode_timer >= self.chase_duration:
#                 self.current_phase = "scatter"
#                 self.mode_timer = 0
#         
#         # Choose movement based on ghost mode
#         if self.agent.ghost_mode == "returning":
#             # Move directly to start position
#             new_pos = self._return_to_home(current_pos)
#             logger.info(f"Ghost {self.agent.ghost_name} returning home")
#         elif self.agent.ghost_mode == "frightened":
#             # Flee from PacMan
#             new_pos = self._flee_from_pacman(current_pos, pacman_pos)
#             logger.info(f"Ghost {self.agent.ghost_name} fleeing from PacMan")
#         else:  # normal mode
#             if self.current_phase == "scatter":
#                 # Move to scatter corner
#                 new_pos = self._move_to_target(current_pos, self.agent.scatter_target)
#                 logger.info(f"Ghost {self.agent.ghost_name} in scatter mode")
#             else:  # chase mode
#                 # Chase PacMan (override in subclasses for unique behaviors)
#                 new_pos = self._chase_pacman(current_pos, pacman_pos)
#                 logger.info(f"Ghost {self.agent.ghost_name} chasing PacMan")
#         
#         # Update position if we got a valid move
#         if new_pos and new_pos != current_pos:
#             self.last_position = current_pos
#             self.agent.position = new_pos
#             self.agent.blackboard.update_agent_position(f"ghost_{self.agent.ghost_name}", new_pos)
#             logger.info(f"Ghost {self.agent.ghost_name} moved to {new_pos}")
#     
#     def _get_best_move_to_target(self, current_pos, target_pos):
#         """Find the best move to reach a target position"""
#         if not target_pos:
#             return None
#         
#         cx, cy = current_pos
#         tx, ty = target_pos
#         
#         # Get all valid moves from current position
#         valid_moves = []
#         for direction, (dx, dy) in DIRECTIONS.items():
#             new_x, new_y = cx + dx, cy + dy
#             if self.agent.maze.is_valid_position(new_x, new_y):
#                 # Avoid going back to the last position (prevent oscillation)
#                 if self.last_position is None or (new_x, new_y) != self.last_position:
#                     # Calculate Manhattan distance to target from this new position
#                     distance = abs(new_x - tx) + abs(new_y - ty)
#                     valid_moves.append((direction, (new_x, new_y), distance))
#         
#         if not valid_moves:
#             # If no moves avoiding last position, consider all valid moves
#             for direction, (dx, dy) in DIRECTIONS.items():
#                 new_x, new_y = cx + dx, cy + dy
#                 if self.agent.maze.is_valid_position(new_x, new_y):
#                     distance = abs(new_x - tx) + abs(new_y - ty)
#                     valid_moves.append((direction, (new_x, new_y), distance))
#         
#         if valid_moves:
#             # Sort by distance and choose the move that gets closest to target
#             valid_moves.sort(key=lambda x: x[2])
#             return valid_moves[0][1]
#         
#         return current_pos
#     
#     def _move_to_target(self, current_pos, target_pos):
#         """Move towards a specific target position"""
#         return self._get_best_move_to_target(current_pos, target_pos)
#     
#     def _chase_pacman(self, ghost_pos, pacman_pos):
#         """Default chase behavior - move directly towards PacMan"""
#         return self._move_to_target(ghost_pos, pacman_pos)
#     
#     def _return_to_home(self, current_pos):
#         """Return to starting position"""
#         return self._move_to_target(current_pos, self.agent.start_position)
#     
#     def _flee_from_pacman(self, ghost_pos, pacman_pos):
#         """Flee behavior - move away from PacMan with some randomness"""
#         if not pacman_pos:
#             return self._random_move(ghost_pos)
#         
#         gx, gy = ghost_pos
#         px, py = pacman_pos
#         
#         # Get all valid moves from current position
#         valid_moves = []
#         for direction, (dx, dy) in DIRECTIONS.items():
#             new_x, new_y = gx + dx, gy + dy
#             if self.agent.maze.is_valid_position(new_x, new_y):
#                 # Avoid going back to the last position
#                 if self.last_position is None or (new_x, new_y) != self.last_position:
#                     # Calculate Manhattan distance to PacMan from this new position
#                     distance = abs(new_x - px) + abs(new_y - py)
#                     valid_moves.append((direction, (new_x, new_y), distance))
#         
#         if valid_moves:
#             # Sort by distance and choose the move that gets furthest from PacMan
#             valid_moves.sort(key=lambda x: x[2], reverse=True)
#             
#             # Add some randomness to fleeing behavior
#             if len(valid_moves) > 1 and random.random() < 0.3:
#                 # 30% chance to take second-best move for unpredictability
#                 return valid_moves[1][1]
#             
#             return valid_moves[0][1]
#         
#         return self._random_move(ghost_pos)
#     
#     def _random_move(self, current_pos):
#         """Fallback random movement with oscillation prevention"""
#         x, y = current_pos
#         valid_moves = []
#         
#         for direction, (dx, dy) in DIRECTIONS.items():
#             new_x, new_y = x + dx, y + dy
#             if self.agent.maze.is_valid_position(new_x, new_y):
#                 # Prefer moves that don't go back to last position
#                 if self.last_position is None or (new_x, new_y) != self.last_position:
#                     valid_moves.append((direction, (new_x, new_y)))
#         
#         # If no moves avoid last position, include all valid moves
#         if not valid_moves:
#             for direction, (dx, dy) in DIRECTIONS.items():
#                 new_x, new_y = x + dx, y + dy
#                 if self.agent.maze.is_valid_position(new_x, new_y):
#                     valid_moves.append((direction, (new_x, new_y)))
#         
#         if valid_moves:
#             chosen = random.choice(valid_moves)
#             return chosen[1]
#         
#         return current_pos
# 
# 
# class BlinkyBehaviour(GhostBehaviour):
#     """Blinky (Red) - The direct chaser"""
#     def _chase_pacman(self, ghost_pos, pacman_pos):
#         """Blinky directly targets PacMan's current position"""
#         return super()._chase_pacman(ghost_pos, pacman_pos)
# 
# 
# class PinkyBehaviour(GhostBehaviour):
#     """Pinky (Pink) - The ambusher"""
#     def _chase_pacman(self, ghost_pos, pacman_pos):
#         """Pinky targets 4 tiles ahead of PacMan's current direction"""
#         if not pacman_pos:
#             return self._random_move(ghost_pos)
#         
#         # Get PacMan's last direction from position history
#         # For now, we'll estimate based on movement pattern
#         # In a full implementation, you'd track PacMan's facing direction
#         px, py = pacman_pos
#         
#         # Try to intercept PacMan by targeting ahead of their position
#         # We'll use a simple prediction based on recent movement
#         target_offset = 4
#         
#         # For now, target 4 tiles in each direction and pick the best
#         potential_targets = [
#             (px + target_offset, py),    # Right
#             (px - target_offset, py),    # Left
#             (px, py - target_offset),    # Up
#             (px, py + target_offset),    # Down
#         ]
#         
#         # Filter valid targets
#         valid_targets = []
#         for tx, ty in potential_targets:
#             if 0 <= tx < self.agent.maze.width and 0 <= ty < self.agent.maze.height:
#                 if not self.agent.maze.is_wall(tx, ty):
#                     valid_targets.append((tx, ty))
#         
#         # If we have valid intercept points, choose the closest one
#         if valid_targets:
#             gx, gy = ghost_pos
#             best_target = min(valid_targets, key=lambda t: abs(t[0] - gx) + abs(t[1] - gy))
#             return self._move_to_target(ghost_pos, best_target)
#         
#         # Fallback to direct chase
#         return super()._chase_pacman(ghost_pos, pacman_pos)
# 
# 
# class InkyBehaviour(GhostBehaviour):
#     """Inky (Cyan) - The flanker"""
#     def _chase_pacman(self, ghost_pos, pacman_pos):
#         """Inky uses both Blinky's position and PacMan's position for complex targeting"""
#         if not pacman_pos:
#             return self._random_move(ghost_pos)
#         
#         # Get Blinky's position
#         blinky_pos = self.agent.blackboard.get_agent_position('ghost_blinky')
#         if not blinky_pos:
#             # If Blinky isn't available, fall back to direct chase
#             return super()._chase_pacman(ghost_pos, pacman_pos)
#         
#         px, py = pacman_pos
#         bx, by = blinky_pos
#         
#         # Inky's target is calculated as:
#         # 1. Get vector from Blinky to 2 tiles ahead of PacMan
#         # 2. Double that vector from Blinky's position
#         
#         # For simplicity, we'll target the opposite side of PacMan from Blinky
#         # This creates a pincer movement
#         target_x = 2 * px - bx
#         target_y = 2 * py - by
#         
#         # Clamp to maze boundaries
#         target_x = max(0, min(target_x, self.agent.maze.width - 1))
#         target_y = max(0, min(target_y, self.agent.maze.height - 1))
#         
#         # If target is in a wall, find nearest valid position
#         if self.agent.maze.is_wall(target_x, target_y):
#             # Search for nearby valid position
#             for dx in [-1, 0, 1]:
#                 for dy in [-1, 0, 1]:
#                     test_x, test_y = target_x + dx, target_y + dy
#                     if (0 <= test_x < self.agent.maze.width and 
#                         0 <= test_y < self.agent.maze.height and 
#                         not self.agent.maze.is_wall(test_x, test_y)):
#                         target_x, target_y = test_x, test_y
#                         break
#         
#         return self._move_to_target(ghost_pos, (target_x, target_y))
# 
# 
# class ClydeBehaviour(GhostBehaviour):
#     """Clyde (Orange) - The alternator"""
#     def _chase_pacman(self, ghost_pos, pacman_pos):
#         """Clyde chases when far away but retreats to corner when close"""
#         if not pacman_pos:
#             return self._random_move(ghost_pos)
#         
#         gx, gy = ghost_pos
#         px, py = pacman_pos
#         
#         # Calculate distance to PacMan
#         distance = abs(gx - px) + abs(gy - py)
#         
#         # If within 8 tiles, retreat to scatter corner
#         if distance < 8:
#             return self._move_to_target(ghost_pos, self.agent.scatter_target)
#         else:
#             # Otherwise, chase like Blinky
#             return super()._chase_pacman(ghost_pos, pacman_pos)

import asyncio
import random
import logging
from spade.behaviour import PeriodicBehaviour
from config.game_config import DIRECTIONS
from behaviors.messaging_behaviors import StateQueryBehaviour

logger = logging.getLogger('PacManMAS.GhostBehavior')

class GhostBehaviour(PeriodicBehaviour, StateQueryBehaviour):
    """Base ghost behavior class"""
    def __init__(self, agent):
        super().__init__(period=0.2)  # Same speed as PacMan
        self.agent = agent
        self.last_position = None  # Track last position to avoid getting stuck
        self.mode_timer = 0
        self.scatter_duration = 70  # 7 seconds in scatter mode
        self.chase_duration = 200   # 20 seconds in chase mode
        self.current_phase = "scatter"  # Start in scatter mode
        self.pacman_position_cache = None
        self.cache_age = 0
    
    async def run(self):
        # Update respawn timer
        self.agent.update_respawn()
        
        # Check if ghost was consumed and needs to reset
        if self.agent.coordinator.is_ghost_consumed(self.agent.ghost_name):
            self.agent.position = self.agent.start_position
            self.agent.ghost_mode = "returning"
            self.agent.respawn_timer = 25  # 5 seconds
            self.agent.coordinator.clear_ghost_consumed(self.agent.ghost_name)
            logger.info(f"Ghost {self.agent.ghost_name} resetting position after being consumed")
            # Update our position immediately
            self.agent.update_position(self.agent.position)
            return  # Skip normal movement this cycle
        
        # Check if we're still respawning
        if self.agent.respawn_timer > 0:
            return  # Don't move while respawning
        
        # Check if this ghost should be frightened
        game_state = self.agent.get_cached_game_state()
        power_active = game_state.get('power_pellet_active', False)
        
        if power_active and self.agent.ghost_mode != "returning":
            if self.agent.ghost_mode != "frightened":
                self.agent.set_mode("frightened")
        else:
            if self.agent.ghost_mode == "frightened":
                self.agent.set_mode("normal")
        
        current_pos = self.agent.position
        
        # Get PacMan's position for AI decisions
        pacman_pos = await self._get_pacman_position()
        
        logger.info(f"Ghost {self.agent.ghost_name} at {current_pos}, mode: {self.agent.ghost_mode}")
        
        # Update scatter/chase phase timer (only in normal mode)
        if self.agent.ghost_mode == "normal":
            self.mode_timer += 1
            if self.current_phase == "scatter" and self.mode_timer >= self.scatter_duration:
                self.current_phase = "chase"
                self.mode_timer = 0
            elif self.current_phase == "chase" and self.mode_timer >= self.chase_duration:
                self.current_phase = "scatter"
                self.mode_timer = 0
        
        # Choose movement based on ghost mode
        if self.agent.ghost_mode == "returning":
            # Move directly to start position
            new_pos = self._return_to_home(current_pos)
            logger.info(f"Ghost {self.agent.ghost_name} returning home")
        elif self.agent.ghost_mode == "frightened":
            # Flee from PacMan
            new_pos = self._flee_from_pacman(current_pos, pacman_pos)
            logger.info(f"Ghost {self.agent.ghost_name} fleeing from PacMan")
        else:  # normal mode
            if self.current_phase == "scatter":
                # Move to scatter corner
                new_pos = self._move_to_target(current_pos, self.agent.scatter_target)
                logger.info(f"Ghost {self.agent.ghost_name} in scatter mode")
            else:  # chase mode
                # Chase PacMan (override in subclasses for unique behaviors)
                new_pos = self._chase_pacman(current_pos, pacman_pos)
                logger.info(f"Ghost {self.agent.ghost_name} chasing PacMan")
        
        # Update position if we got a valid move
        if new_pos and new_pos != current_pos:
            self.last_position = current_pos
            self.agent.update_position(new_pos)
            logger.info(f"Ghost {self.agent.ghost_name} moved to {new_pos}")
    
    async def _get_pacman_position(self):
        """Get PacMan's position from cache or query if stale"""
        # Try cached position first
        pacman_pos = self.agent.get_cached_agent_position('pacman')
        
        if pacman_pos:
            return pacman_pos
        
        # Cache miss or stale - try to query
        self.cache_age += 1
        if self.cache_age > 5:  # Query every 5 cycles if no cached position
            try:
                pacman_pos = await self.query_agent_position('pacman', timeout=0.3)
                if pacman_pos:
                    self.pacman_position_cache = pacman_pos
                    self.cache_age = 0
                    return pacman_pos
            except Exception as e:
                logger.warning(f"Failed to query PacMan position: {e}")
        
        # Return last known position or None
        return self.pacman_position_cache
    
    def _get_best_move_to_target(self, current_pos, target_pos):
        """Find the best move to reach a target position"""
        if not target_pos:
            return None
        
        cx, cy = current_pos
        tx, ty = target_pos
        
        # Get all valid moves from current position
        valid_moves = []
        for direction, (dx, dy) in DIRECTIONS.items():
            new_x, new_y = cx + dx, cy + dy
            if self.agent.maze.is_valid_position(new_x, new_y):
                # Avoid going back to the last position (prevent oscillation)
                if self.last_position is None or (new_x, new_y) != self.last_position:
                    # Calculate Manhattan distance to target from this new position
                    distance = abs(new_x - tx) + abs(new_y - ty)
                    valid_moves.append((direction, (new_x, new_y), distance))
        
        if not valid_moves:
            # If no moves avoiding last position, consider all valid moves
            for direction, (dx, dy) in DIRECTIONS.items():
                new_x, new_y = cx + dx, cy + dy
                if self.agent.maze.is_valid_position(new_x, new_y):
                    distance = abs(new_x - tx) + abs(new_y - ty)
                    valid_moves.append((direction, (new_x, new_y), distance))
        
        if valid_moves:
            # Sort by distance and choose the move that gets closest to target
            valid_moves.sort(key=lambda x: x[2])
            return valid_moves[0][1]
        
        return current_pos
    
    def _move_to_target(self, current_pos, target_pos):
        """Move towards a specific target position"""
        return self._get_best_move_to_target(current_pos, target_pos)
    
    def _chase_pacman(self, ghost_pos, pacman_pos):
        """Default chase behavior - move directly towards PacMan"""
        return self._move_to_target(ghost_pos, pacman_pos)
    
    def _return_to_home(self, current_pos):
        """Return to starting position"""
        return self._move_to_target(current_pos, self.agent.start_position)
    
    def _flee_from_pacman(self, ghost_pos, pacman_pos):
        """Flee behavior - move away from PacMan with some randomness"""
        if not pacman_pos:
            return self._random_move(ghost_pos)
        
        gx, gy = ghost_pos
        px, py = pacman_pos
        
        # Get all valid moves from current position
        valid_moves = []
        for direction, (dx, dy) in DIRECTIONS.items():
            new_x, new_y = gx + dx, gy + dy
            if self.agent.maze.is_valid_position(new_x, new_y):
                # Avoid going back to the last position
                if self.last_position is None or (new_x, new_y) != self.last_position:
                    # Calculate Manhattan distance to PacMan from this new position
                    distance = abs(new_x - px) + abs(new_y - py)
                    valid_moves.append((direction, (new_x, new_y), distance))
        
        if valid_moves:
            # Sort by distance and choose the move that gets furthest from PacMan
            valid_moves.sort(key=lambda x: x[2], reverse=True)
            
            # Add some randomness to fleeing behavior
            if len(valid_moves) > 1 and random.random() < 0.3:
                # 30% chance to take second-best move for unpredictability
                return valid_moves[1][1]
            
            return valid_moves[0][1]
        
        return self._random_move(ghost_pos)
    
    def _random_move(self, current_pos):
        """Fallback random movement with oscillation prevention"""
        x, y = current_pos
        valid_moves = []
        
        for direction, (dx, dy) in DIRECTIONS.items():
            new_x, new_y = x + dx, y + dy
            if self.agent.maze.is_valid_position(new_x, new_y):
                # Prefer moves that don't go back to last position
                if self.last_position is None or (new_x, new_y) != self.last_position:
                    valid_moves.append((direction, (new_x, new_y)))
        
        # If no moves avoid last position, include all valid moves
        if not valid_moves:
            for direction, (dx, dy) in DIRECTIONS.items():
                new_x, new_y = x + dx, y + dy
                if self.agent.maze.is_valid_position(new_x, new_y):
                    valid_moves.append((direction, (new_x, new_y)))
        
        if valid_moves:
            chosen = random.choice(valid_moves)
            return chosen[1]
        
        return current_pos


class BlinkyBehaviour(GhostBehaviour):
    """Blinky (Red) - The direct chaser"""
    def _chase_pacman(self, ghost_pos, pacman_pos):
        """Blinky directly targets PacMan's current position"""
        return super()._chase_pacman(ghost_pos, pacman_pos)


class PinkyBehaviour(GhostBehaviour):
    """Pinky (Pink) - The ambusher"""
    def _chase_pacman(self, ghost_pos, pacman_pos):
        """Pinky targets 4 tiles ahead of PacMan's current direction"""
        if not pacman_pos:
            return self._random_move(ghost_pos)
        
        px, py = pacman_pos
        
        # Try to intercept PacMan by targeting ahead of their position
        target_offset = 4
        
        # For now, target 4 tiles in each direction and pick the best
        potential_targets = [
            (px + target_offset, py),    # Right
            (px - target_offset, py),    # Left
            (px, py - target_offset),    # Up
            (px, py + target_offset),    # Down
        ]
        
        # Filter valid targets
        valid_targets = []
        for tx, ty in potential_targets:
            if 0 <= tx < self.agent.maze.width and 0 <= ty < self.agent.maze.height:
                if not self.agent.maze.is_wall(tx, ty):
                    valid_targets.append((tx, ty))
        
        # If we have valid intercept points, choose the closest one
        if valid_targets:
            gx, gy = ghost_pos
            best_target = min(valid_targets, key=lambda t: abs(t[0] - gx) + abs(t[1] - gy))
            return self._move_to_target(ghost_pos, best_target)
        
        # Fallback to direct chase
        return super()._chase_pacman(ghost_pos, pacman_pos)


class InkyBehaviour(GhostBehaviour):
    """Inky (Cyan) - The flanker"""
    def _chase_pacman(self, ghost_pos, pacman_pos):
        """Inky uses both Blinky's position and PacMan's position for complex targeting"""
        if not pacman_pos:
            return self._random_move(ghost_pos)
        
        # Get Blinky's position from cache
        blinky_pos = self.agent.get_cached_agent_position('ghost_blinky')
        if not blinky_pos:
            # If Blinky isn't available, fall back to direct chase
            return super()._chase_pacman(ghost_pos, pacman_pos)
        
        px, py = pacman_pos
        bx, by = blinky_pos
        
        # Inky's target is calculated as:
        # 1. Get vector from Blinky to 2 tiles ahead of PacMan
        # 2. Double that vector from Blinky's position
        
        # For simplicity, we'll target the opposite side of PacMan from Blinky
        # This creates a pincer movement
        target_x = 2 * px - bx
        target_y = 2 * py - by
        
        # Clamp to maze boundaries
        target_x = max(0, min(target_x, self.agent.maze.width - 1))
        target_y = max(0, min(target_y, self.agent.maze.height - 1))
        
        # If target is in a wall, find nearest valid position
        if self.agent.maze.is_wall(target_x, target_y):
            # Search for nearby valid position
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    test_x, test_y = target_x + dx, target_y + dy
                    if (0 <= test_x < self.agent.maze.width and 
                        0 <= test_y < self.agent.maze.height and 
                        not self.agent.maze.is_wall(test_x, test_y)):
                        target_x, target_y = test_x, test_y
                        break
        
        return self._move_to_target(ghost_pos, (target_x, target_y))


class ClydeBehaviour(GhostBehaviour):
    """Clyde (Orange) - The alternator"""
    def _chase_pacman(self, ghost_pos, pacman_pos):
        """Clyde chases when far away but retreats to corner when close"""
        if not pacman_pos:
            return self._random_move(ghost_pos)
        
        gx, gy = ghost_pos
        px, py = pacman_pos
        
        # Calculate distance to PacMan
        distance = abs(gx - px) + abs(gy - py)
        
        # If within 8 tiles, retreat to scatter corner
        if distance < 8:
            return self._move_to_target(ghost_pos, self.agent.scatter_target)
        else:
            # Otherwise, chase like Blinky
            return super()._chase_pacman(ghost_pos, pacman_pos)
