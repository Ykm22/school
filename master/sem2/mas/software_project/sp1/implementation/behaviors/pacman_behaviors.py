# import asyncio
# import random
# import logging
# from spade.behaviour import PeriodicBehaviour
# from config.game_config import DIRECTIONS
# 
# logger = logging.getLogger('PacManMAS.PacManBehavior')
# 
# class SmartPacManBehaviour(PeriodicBehaviour):
#     def __init__(self, agent):
#         super().__init__(period=0.2)  # 0.2 seconds between moves
#         self.agent = agent
#         self.last_position = None
#         self.stuck_counter = 0
#         
#     async def run(self):
#         current_pos = self.agent.position
#         x, y = current_pos
#         
#         logger.info(f"Pac-Man at position {current_pos}, planning next move...")
#         
#         # Check and collect item at current position first
#         collected_item = self.agent.maze.collect_item(x, y)
#         if collected_item == 'dot':
#             self.agent.blackboard.collect_dot()
#         elif collected_item == 'power_pellet':
#             self.agent.blackboard.collect_power_pellet()
#         
#         # Check if game is complete
#         if self.agent.maze.is_game_complete():
#             logger.info("All collectibles gathered! Game complete!")
#             self.agent.blackboard.set_game_complete()
#             return
#         
#         # Get game state for decision making
#         game_state = self.agent.blackboard.get_game_state()
#         power_active = game_state.get('power_pellet_active', False)
#         
#         # Get ghost positions
#         ghost_positions = self._get_ghost_positions()
# 
#         # Check for immediate collision with ghosts
#         for ghost_pos in ghost_positions:
#             if ghost_pos == current_pos and not power_active:
#                 logger.info(f"Pac-Man caught by ghost at {current_pos}!")
#                 self.agent.blackboard.set_game_over()
#                 return
#         
#         # Determine best move based on current situation
#         if power_active:
#             # Power mode - hunt ghosts!
#             best_move = self._hunt_ghosts(current_pos, ghost_positions)
#             logger.info("Pac-Man in POWER MODE - hunting ghosts!")
#         else:
#             # Normal mode - balance between collecting dots and avoiding ghosts
#             danger_level = self._assess_danger(current_pos, ghost_positions)
#             
#             if danger_level > 0.7:
#                 # High danger - prioritize escape
#                 best_move = self._escape_ghosts(current_pos, ghost_positions)
#                 logger.info("Pac-Man in DANGER - escaping ghosts!")
#             elif danger_level > 0.3:
#                 # Medium danger - careful collection
#                 best_move = self._safe_collect(current_pos, ghost_positions)
#                 logger.info("Pac-Man being CAUTIOUS - safe collection")
#             else:
#                 # Low danger - focus on efficient collection
#                 best_move = self._efficient_collect(current_pos)
#                 logger.info("Pac-Man COLLECTING - efficient path")
#         
#         # Execute the chosen move
#         if best_move and best_move != current_pos:
#             self.last_position = current_pos
#             self.agent.position = best_move
#             self.agent.blackboard.update_agent_position(self.agent.agent_name, self.agent.position)
#             
#             direction = self._get_direction_name(current_pos, best_move)
#             logger.info(f"Pac-Man moved {direction} to position {self.agent.position}")
#             self.stuck_counter = 0
#         else:
#             # No good move found, try random valid move
#             self.stuck_counter += 1
#             if self.stuck_counter > 3:
#                 random_move = self._get_random_valid_move(current_pos)
#                 if random_move:
#                     self.agent.position = random_move
#                     self.agent.blackboard.update_agent_position(self.agent.agent_name, self.agent.position)
#                     logger.warning(f"Pac-Man was stuck, made random move to {random_move}")
#                     self.stuck_counter = 0
#         
#         # Increment game step
#         self.agent.blackboard.increment_step()
#     
#     def _get_ghost_positions(self):
#         """Get all ghost positions from blackboard"""
#         positions = self.agent.blackboard.get_all_positions()
#         ghost_positions = []
#         for agent_name, pos in positions.items():
#             if agent_name.startswith('ghost_'):
#                 ghost_positions.append(pos)
#         return ghost_positions
#     
#     def _assess_danger(self, pac_pos, ghost_positions):
#         """Assess danger level based on ghost proximity (0.0 to 1.0)"""
#         if not ghost_positions:
#             return 0.0
#         
#         px, py = pac_pos
#         min_distance = float('inf')
#         
#         for gx, gy in ghost_positions:
#             distance = abs(px - gx) + abs(py - gy)
#             min_distance = min(min_distance, distance)
#         
#         # Convert distance to danger level (closer = higher danger)
#         if min_distance <= 2:
#             return 1.0
#         elif min_distance <= 4:
#             return 0.8
#         elif min_distance <= 6:
#             return 0.5
#         elif min_distance <= 8:
#             return 0.3
#         else:
#             return 0.1
#     
#     def _hunt_ghosts(self, pac_pos, ghost_positions):
#         """When powered up, chase the nearest ghost"""
#         if not ghost_positions:
#             return self._efficient_collect(pac_pos)
#         
#         # Find nearest ghost
#         px, py = pac_pos
#         nearest_ghost = None
#         min_distance = float('inf')
#         
#         for ghost_pos in ghost_positions:
#             gx, gy = ghost_pos
#             distance = abs(px - gx) + abs(py - gy)
#             if distance < min_distance:
#                 min_distance = distance
#                 nearest_ghost = ghost_pos
#         
#         if nearest_ghost:
#             # Move towards nearest ghost
#             return self._move_towards_target(pac_pos, nearest_ghost)
#         
#         return self._efficient_collect(pac_pos)
#     
#     def _escape_ghosts(self, pac_pos, ghost_positions):
#         """Find the safest direction away from ghosts"""
#         px, py = pac_pos
#         valid_moves = self.agent.maze.get_valid_moves(px, py)
#         
#         if not valid_moves:
#             return None
#         
#         # Score each valid move based on distance from ghosts
#         move_scores = []
#         for direction in valid_moves:
#             dx, dy = DIRECTIONS[direction]
#             new_pos = (px + dx, py + dy)
#             
#             # Skip if going back to last position (avoid oscillation)
#             if self.last_position and new_pos == self.last_position:
#                 continue
#             
#             # Calculate minimum distance to any ghost from this position
#             min_ghost_distance = float('inf')
#             for ghost_pos in ghost_positions:
#                 gx, gy = ghost_pos
#                 distance = abs(new_pos[0] - gx) + abs(new_pos[1] - gy)
#                 min_ghost_distance = min(min_ghost_distance, distance)
#             
#             # Also check if there's a power pellet nearby
#             power_pellet_bonus = 0
#             if self._is_power_pellet_nearby(new_pos):
#                 power_pellet_bonus = 3  # Bonus for escape route with power pellet
#             
#             move_scores.append((new_pos, min_ghost_distance + power_pellet_bonus))
#         
#         if move_scores:
#             # Choose move that maximizes distance from ghosts
#             move_scores.sort(key=lambda x: x[1], reverse=True)
#             return move_scores[0][0]
#         
#         return self._get_random_valid_move(pac_pos)
#     
#     def _safe_collect(self, pac_pos, ghost_positions):
#         """Collect dots while maintaining safe distance from ghosts"""
#         px, py = pac_pos
#         valid_moves = self.agent.maze.get_valid_moves(px, py)
#         
#         if not valid_moves:
#             return None
#         
#         # Score each move based on dots and safety
#         move_scores = []
#         for direction in valid_moves:
#             dx, dy = DIRECTIONS[direction]
#             new_pos = (px + dx, py + dy)
#             
#             # Skip if going back to last position
#             if self.last_position and new_pos == self.last_position:
#                 continue
#             
#             # Check if there's a collectible at this position
#             cell = self.agent.maze.get_cell(new_pos[0], new_pos[1])
#             collectible_score = 0
#             if cell == '.':
#                 collectible_score = 10
#             elif cell == 'O':
#                 # Only go for power pellet if ghosts are somewhat close
#                 danger = self._assess_danger(new_pos, ghost_positions)
#                 if danger > 0.3:
#                     collectible_score = 20  # High value if we need it
#                 else:
#                     collectible_score = 5   # Lower value if we don't
#             
#             # Calculate safety score (distance from ghosts)
#             min_ghost_distance = float('inf')
#             for ghost_pos in ghost_positions:
#                 gx, gy = ghost_pos
#                 distance = abs(new_pos[0] - gx) + abs(new_pos[1] - gy)
#                 min_ghost_distance = min(min_ghost_distance, distance)
#             
#             # Combine scores (balance collection and safety)
#             safety_weight = 2.0  # How much we value safety vs collection
#             total_score = collectible_score + (min_ghost_distance * safety_weight)
#             
#             move_scores.append((new_pos, total_score))
#         
#         if move_scores:
#             move_scores.sort(key=lambda x: x[1], reverse=True)
#             return move_scores[0][0]
#         
#         return self._get_random_valid_move(pac_pos)
#     
#     def _efficient_collect(self, pac_pos):
#         """Efficiently collect dots when safe"""
#         px, py = pac_pos
#         valid_moves = self.agent.maze.get_valid_moves(px, py)
#         
#         if not valid_moves:
#             return None
#         
#         # Look for nearby dots and power pellets
#         move_scores = []
#         for direction in valid_moves:
#             dx, dy = DIRECTIONS[direction]
#             new_pos = (px + dx, py + dy)
#             
#             # Skip if going back to last position
#             if self.last_position and new_pos == self.last_position:
#                 continue
#             
#             score = 0
#             
#             # Check immediate cell
#             cell = self.agent.maze.get_cell(new_pos[0], new_pos[1])
#             if cell == '.':
#                 score += 10
#             elif cell == 'O':
#                 score += 5  # Lower priority when safe
#             
#             # Look ahead for more dots (planning)
#             dots_nearby = self._count_dots_nearby(new_pos, depth=3)
#             score += dots_nearby * 2
#             
#             move_scores.append((new_pos, score))
#         
#         if move_scores:
#             # Add some randomness to avoid predictable patterns
#             move_scores.sort(key=lambda x: x[1], reverse=True)
#             
#             # Sometimes take second-best move for variety
#             if len(move_scores) > 1 and random.random() < 0.2:
#                 return move_scores[1][0]
#             
#             return move_scores[0][0]
#         
#         return self._get_random_valid_move(pac_pos)
#     
#     def _move_towards_target(self, current_pos, target_pos):
#         """Move towards a specific target position"""
#         cx, cy = current_pos
#         tx, ty = target_pos
#         
#         valid_moves = self.agent.maze.get_valid_moves(cx, cy)
#         if not valid_moves:
#             return None
#         
#         # Find move that gets closest to target
#         best_move = None
#         min_distance = float('inf')
#         
#         for direction in valid_moves:
#             dx, dy = DIRECTIONS[direction]
#             new_pos = (cx + dx, cy + dy)
#             
#             # Skip if going back to last position
#             if self.last_position and new_pos == self.last_position:
#                 continue
#             
#             distance = abs(new_pos[0] - tx) + abs(new_pos[1] - ty)
#             if distance < min_distance:
#                 min_distance = distance
#                 best_move = new_pos
#         
#         return best_move
#     
#     def _count_dots_nearby(self, pos, depth=2):
#         """Count dots within a certain depth from position"""
#         if depth <= 0:
#             return 0
#         
#         x, y = pos
#         count = 0
#         
#         # Check all directions
#         for dx, dy in DIRECTIONS.values():
#             new_x, new_y = x + dx, y + dy
#             if self.agent.maze.is_valid_position(new_x, new_y):
#                 cell = self.agent.maze.get_cell(new_x, new_y)
#                 if cell == '.':
#                     count += 1
#                 # Recursively check further
#                 if depth > 1:
#                     count += self._count_dots_nearby((new_x, new_y), depth - 1) * 0.5
#         
#         return count
#     
#     def _is_power_pellet_nearby(self, pos, radius=3):
#         """Check if there's a power pellet within radius"""
#         x, y = pos
#         
#         for dx in range(-radius, radius + 1):
#             for dy in range(-radius, radius + 1):
#                 check_x, check_y = x + dx, y + dy
#                 if self.agent.maze.is_valid_position(check_x, check_y):
#                     if self.agent.maze.get_cell(check_x, check_y) == 'O':
#                         return True
#         return False
#     
#     def _get_random_valid_move(self, current_pos):
#         """Get a random valid move from current position"""
#         x, y = current_pos
#         valid_moves = self.agent.maze.get_valid_moves(x, y)
#         
#         if valid_moves:
#             direction = random.choice(valid_moves)
#             dx, dy = DIRECTIONS[direction]
#             return (x + dx, y + dy)
#         
#         return None
#     
#     def _get_direction_name(self, from_pos, to_pos):
#         """Get the direction name for a move"""
#         fx, fy = from_pos
#         tx, ty = to_pos
#         
#         dx = tx - fx
#         dy = ty - fy
#         
#         if dx > 0:
#             return "RIGHT"
#         elif dx < 0:
#             return "LEFT"
#         elif dy > 0:
#             return "DOWN"
#         elif dy < 0:
#             return "UP"
#         else:
#             return "NONE"
# 
# 
# class RandomMoveBehaviour(PeriodicBehaviour):
#     """Original random movement behavior for testing"""
#     def __init__(self, agent):
#         super().__init__(period=0.2)  # 0.2 seconds between moves
#         self.agent = agent
#     
#     async def run(self):
#         current_pos = self.agent.position
#         x, y = current_pos
#         
#         logger.info(f"Pac-Man at position {current_pos}, planning next move...")
#         
#         # Check and collect item at current position first
#         collected_item = self.agent.maze.collect_item(x, y)
#         if collected_item == 'dot':
#             self.agent.blackboard.collect_dot()
#         elif collected_item == 'power_pellet':
#             self.agent.blackboard.collect_power_pellet()
#         
#         # Check if game is complete
#         if self.agent.maze.is_game_complete():
#             logger.info("All collectibles gathered! Game complete!")
#             self.agent.blackboard.set_game_complete()
#             return
#         
#         # Get valid moves
#         valid_moves = self.agent.maze.get_valid_moves(x, y)
#         
#         if valid_moves:
#             # Choose random valid move
#             chosen_direction = random.choice(valid_moves)
#             dx, dy = DIRECTIONS[chosen_direction]
#             new_x, new_y = x + dx, y + dy
#             
#             # Update position
#             self.agent.position = (new_x, new_y)
#             self.agent.blackboard.update_agent_position(self.agent.agent_name, self.agent.position)
#             
#             logger.info(f"Pac-Man moved {chosen_direction} to position {self.agent.position}")
#         else:
#             logger.warning(f"Pac-Man has no valid moves from position {current_pos}")
#         
#         # Increment game step
#         self.agent.blackboard.increment_step()

import asyncio
import random
import logging
from spade.behaviour import PeriodicBehaviour
from config.game_config import DIRECTIONS
from behaviors.messaging_behaviors import GameEventBroadcastBehaviour, StateQueryBehaviour

logger = logging.getLogger('PacManMAS.PacManBehavior')

class SmartPacManBehaviour(PeriodicBehaviour, GameEventBroadcastBehaviour, StateQueryBehaviour):
    def __init__(self, agent):
        super().__init__(period=0.2)
        self.agent = agent
        self.last_position = None
        self.stuck_counter = 0
        self.position_cache_age = 0
        
    async def run(self):
        current_pos = self.agent.position
        x, y = current_pos
        
        logger.info(f"Pac-Man at position {current_pos}, planning next move...")
        
        # Check and collect item at current position first
        collected_item = self.agent.maze.collect_item(x, y)
        if collected_item == 'dot':
            await self.broadcast_game_event('dot_collected', current_pos, 10)
        elif collected_item == 'power_pellet':
            await self.broadcast_game_event('power_pellet_collected', current_pos, 50)
        
        # Check if game is complete
        if self.agent.maze.is_game_complete():
            logger.info("All collectibles gathered! Game complete!")
            await self.broadcast_game_event('game_complete')
            return
        
        # Get game state from local cache
        game_state = self.agent.get_cached_game_state()
        power_active = game_state.get('power_pellet_active', False)
        
        # Get ghost positions from cache, refresh if needed
        ghost_positions = await self._get_ghost_positions()

        # Check for immediate collision with ghosts
        for ghost_pos in ghost_positions:
            if ghost_pos == current_pos and not power_active:
                logger.info(f"Pac-Man caught by ghost at {current_pos}!")
                await self.broadcast_game_event('game_over')
                return
        
        # Determine best move based on current situation
        if power_active:
            best_move = self._hunt_ghosts(current_pos, ghost_positions)
            logger.info("Pac-Man in POWER MODE - hunting ghosts!")
        else:
            danger_level = self._assess_danger(current_pos, ghost_positions)
            
            if danger_level > 0.7:
                best_move = self._escape_ghosts(current_pos, ghost_positions)
                logger.info("Pac-Man in DANGER - escaping ghosts!")
            elif danger_level > 0.3:
                best_move = self._safe_collect(current_pos, ghost_positions)
                logger.info("Pac-Man being CAUTIOUS - safe collection")
            else:
                best_move = self._efficient_collect(current_pos)
                logger.info("Pac-Man COLLECTING - efficient path")
        
        # Execute the chosen move
        if best_move and best_move != current_pos:
            self.last_position = current_pos
            self.agent.update_position(best_move)
            
            direction = self._get_direction_name(current_pos, best_move)
            logger.info(f"Pac-Man moved {direction} to position {self.agent.position}")
            self.stuck_counter = 0
        else:
            # No good move found, try random valid move
            self.stuck_counter += 1
            if self.stuck_counter > 3:
                random_move = self._get_random_valid_move(current_pos)
                if random_move:
                    self.agent.update_position(random_move)
                    logger.warning(f"Pac-Man was stuck, made random move to {random_move}")
                    self.stuck_counter = 0
        
        # Increment game step in coordinator
        self.agent.coordinator.increment_step()
    
    async def _get_ghost_positions(self):
        """Get ghost positions from cache or query if stale"""
        ghost_positions = []
        
        # Try to get positions from local cache first
        cached_positions = self.agent.get_cached_all_positions()
        
        for agent_name, pos in cached_positions.items():
            if agent_name.startswith('ghost_'):
                ghost_positions.append(pos)
        
        # If we have fewer than 4 ghost positions or cache is getting old
        if len(ghost_positions) < 4:
            self.position_cache_age += 1
            
            # Every few cycles, refresh positions via query
            if self.position_cache_age > 10:
                try:
                    fresh_positions = await self.query_all_positions(timeout=0.5)
                    if fresh_positions:
                        ghost_positions = []
                        for agent_name, pos in fresh_positions.items():
                            if agent_name.startswith('ghost_'):
                                ghost_positions.append(pos)
                        self.position_cache_age = 0
                        logger.debug("Refreshed ghost positions via query")
                except Exception as e:
                    logger.warning(f"Failed to refresh positions: {e}")
        
        return ghost_positions
    
    def _assess_danger(self, pac_pos, ghost_positions):
        """Assess danger level based on ghost proximity (0.0 to 1.0)"""
        if not ghost_positions:
            return 0.0
        
        px, py = pac_pos
        min_distance = float('inf')
        
        for gx, gy in ghost_positions:
            distance = abs(px - gx) + abs(py - gy)
            min_distance = min(min_distance, distance)
        
        # Convert distance to danger level (closer = higher danger)
        if min_distance <= 2:
            return 1.0
        elif min_distance <= 4:
            return 0.8
        elif min_distance <= 6:
            return 0.5
        elif min_distance <= 8:
            return 0.3
        else:
            return 0.1
    
    def _hunt_ghosts(self, pac_pos, ghost_positions):
        """When powered up, chase the nearest ghost"""
        if not ghost_positions:
            return self._efficient_collect(pac_pos)
        
        # Find nearest ghost
        px, py = pac_pos
        nearest_ghost = None
        min_distance = float('inf')
        
        for ghost_pos in ghost_positions:
            gx, gy = ghost_pos
            distance = abs(px - gx) + abs(py - gy)
            if distance < min_distance:
                min_distance = distance
                nearest_ghost = ghost_pos
        
        if nearest_ghost:
            # Move towards nearest ghost
            return self._move_towards_target(pac_pos, nearest_ghost)
        
        return self._efficient_collect(pac_pos)
    
    def _escape_ghosts(self, pac_pos, ghost_positions):
        """Find the safest direction away from ghosts"""
        px, py = pac_pos
        valid_moves = self.agent.maze.get_valid_moves(px, py)
        
        if not valid_moves:
            return None
        
        # Score each valid move based on distance from ghosts
        move_scores = []
        for direction in valid_moves:
            dx, dy = DIRECTIONS[direction]
            new_pos = (px + dx, py + dy)
            
            # Skip if going back to last position (avoid oscillation)
            if self.last_position and new_pos == self.last_position:
                continue
            
            # Calculate minimum distance to any ghost from this position
            min_ghost_distance = float('inf')
            for ghost_pos in ghost_positions:
                gx, gy = ghost_pos
                distance = abs(new_pos[0] - gx) + abs(new_pos[1] - gy)
                min_ghost_distance = min(min_ghost_distance, distance)
            
            # Also check if there's a power pellet nearby
            power_pellet_bonus = 0
            if self._is_power_pellet_nearby(new_pos):
                power_pellet_bonus = 3  # Bonus for escape route with power pellet
            
            move_scores.append((new_pos, min_ghost_distance + power_pellet_bonus))
        
        if move_scores:
            # Choose move that maximizes distance from ghosts
            move_scores.sort(key=lambda x: x[1], reverse=True)
            return move_scores[0][0]
        
        return self._get_random_valid_move(pac_pos)
    
    def _safe_collect(self, pac_pos, ghost_positions):
        """Collect dots while maintaining safe distance from ghosts"""
        px, py = pac_pos
        valid_moves = self.agent.maze.get_valid_moves(px, py)
        
        if not valid_moves:
            return None
        
        # Score each move based on dots and safety
        move_scores = []
        for direction in valid_moves:
            dx, dy = DIRECTIONS[direction]
            new_pos = (px + dx, py + dy)
            
            # Skip if going back to last position
            if self.last_position and new_pos == self.last_position:
                continue
            
            # Check if there's a collectible at this position
            cell = self.agent.maze.get_cell(new_pos[0], new_pos[1])
            collectible_score = 0
            if cell == '.':
                collectible_score = 10
            elif cell == 'O':
                # Only go for power pellet if ghosts are somewhat close
                danger = self._assess_danger(new_pos, ghost_positions)
                if danger > 0.3:
                    collectible_score = 20  # High value if we need it
                else:
                    collectible_score = 5   # Lower value if we don't
            
            # Calculate safety score (distance from ghosts)
            min_ghost_distance = float('inf')
            for ghost_pos in ghost_positions:
                gx, gy = ghost_pos
                distance = abs(new_pos[0] - gx) + abs(new_pos[1] - gy)
                min_ghost_distance = min(min_ghost_distance, distance)
            
            # Combine scores (balance collection and safety)
            safety_weight = 2.0  # How much we value safety vs collection
            total_score = collectible_score + (min_ghost_distance * safety_weight)
            
            move_scores.append((new_pos, total_score))
        
        if move_scores:
            move_scores.sort(key=lambda x: x[1], reverse=True)
            return move_scores[0][0]
        
        return self._get_random_valid_move(pac_pos)
    
    def _efficient_collect(self, pac_pos):
        """Efficiently collect dots when safe"""
        px, py = pac_pos
        valid_moves = self.agent.maze.get_valid_moves(px, py)
        
        if not valid_moves:
            return None
        
        # Look for nearby dots and power pellets
        move_scores = []
        for direction in valid_moves:
            dx, dy = DIRECTIONS[direction]
            new_pos = (px + dx, py + dy)
            
            # Skip if going back to last position
            if self.last_position and new_pos == self.last_position:
                continue
            
            score = 0
            
            # Check immediate cell
            cell = self.agent.maze.get_cell(new_pos[0], new_pos[1])
            if cell == '.':
                score += 10
            elif cell == 'O':
                score += 5  # Lower priority when safe
            
            # Look ahead for more dots (planning)
            dots_nearby = self._count_dots_nearby(new_pos, depth=3)
            score += dots_nearby * 2
            
            move_scores.append((new_pos, score))
        
        if move_scores:
            # Add some randomness to avoid predictable patterns
            move_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Sometimes take second-best move for variety
            if len(move_scores) > 1 and random.random() < 0.2:
                return move_scores[1][0]
            
            return move_scores[0][0]
        
        return self._get_random_valid_move(pac_pos)
    
    def _move_towards_target(self, current_pos, target_pos):
        """Move towards a specific target position"""
        cx, cy = current_pos
        tx, ty = target_pos
        
        valid_moves = self.agent.maze.get_valid_moves(cx, cy)
        if not valid_moves:
            return None
        
        # Find move that gets closest to target
        best_move = None
        min_distance = float('inf')
        
        for direction in valid_moves:
            dx, dy = DIRECTIONS[direction]
            new_pos = (cx + dx, cy + dy)
            
            # Skip if going back to last position
            if self.last_position and new_pos == self.last_position:
                continue
            
            distance = abs(new_pos[0] - tx) + abs(new_pos[1] - ty)
            if distance < min_distance:
                min_distance = distance
                best_move = new_pos
        
        return best_move
    
    def _count_dots_nearby(self, pos, depth=2):
        """Count dots within a certain depth from position"""
        if depth <= 0:
            return 0
        
        x, y = pos
        count = 0
        
        # Check all directions
        for dx, dy in DIRECTIONS.values():
            new_x, new_y = x + dx, y + dy
            if self.agent.maze.is_valid_position(new_x, new_y):
                cell = self.agent.maze.get_cell(new_x, new_y)
                if cell == '.':
                    count += 1
                # Recursively check further
                if depth > 1:
                    count += self._count_dots_nearby((new_x, new_y), depth - 1) * 0.5
        
        return count
    
    def _is_power_pellet_nearby(self, pos, radius=3):
        """Check if there's a power pellet within radius"""
        x, y = pos
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                check_x, check_y = x + dx, y + dy
                if self.agent.maze.is_valid_position(check_x, check_y):
                    if self.agent.maze.get_cell(check_x, check_y) == 'O':
                        return True
        return False
    
    def _get_random_valid_move(self, current_pos):
        """Get a random valid move from current position"""
        x, y = current_pos
        valid_moves = self.agent.maze.get_valid_moves(x, y)
        
        if valid_moves:
            direction = random.choice(valid_moves)
            dx, dy = DIRECTIONS[direction]
            return (x + dx, y + dy)
        
        return None
    
    def _get_direction_name(self, from_pos, to_pos):
        """Get the direction name for a move"""
        fx, fy = from_pos
        tx, ty = to_pos
        
        dx = tx - fx
        dy = ty - fy
        
        if dx > 0:
            return "RIGHT"
        elif dx < 0:
            return "LEFT"
        elif dy > 0:
            return "DOWN"
        elif dy < 0:
            return "UP"
        else:
            return "NONE"


class RandomMoveBehaviour(PeriodicBehaviour, GameEventBroadcastBehaviour):
    """Original random movement behavior for testing"""
    def __init__(self, agent):
        super().__init__(period=0.2)
        self.agent = agent
    
    async def run(self):
        current_pos = self.agent.position
        x, y = current_pos
        
        logger.info(f"Pac-Man at position {current_pos}, planning next move...")
        
        # Check and collect item at current position first
        collected_item = self.agent.maze.collect_item(x, y)
        if collected_item == 'dot':
            await self.broadcast_game_event('dot_collected', current_pos, 10)
        elif collected_item == 'power_pellet':
            await self.broadcast_game_event('power_pellet_collected', current_pos, 50)
        
        # Check if game is complete
        if self.agent.maze.is_game_complete():
            logger.info("All collectibles gathered! Game complete!")
            await self.broadcast_game_event('game_complete')
            return
        
        # Get valid moves
        valid_moves = self.agent.maze.get_valid_moves(x, y)
        
        if valid_moves:
            # Choose random valid move
            chosen_direction = random.choice(valid_moves)
            dx, dy = DIRECTIONS[chosen_direction]
            new_x, new_y = x + dx, y + dy
            
            # Update position
            self.agent.update_position((new_x, new_y))
            
            logger.info(f"Pac-Man moved {chosen_direction} to position {self.agent.position}")
        else:
            logger.warning(f"Pac-Man has no valid moves from position {current_pos}")
        
        # Increment game step
        self.agent.coordinator.increment_step()
