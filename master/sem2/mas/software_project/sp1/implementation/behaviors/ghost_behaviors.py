import asyncio
import random
import logging
from spade.behaviour import PeriodicBehaviour
from config.game_config import DIRECTIONS

logger = logging.getLogger('PacManMAS.GhostBehavior')

class GhostBehaviour(PeriodicBehaviour):
    def __init__(self, agent):
        super().__init__(period=0.2)  # Same speed as PacMan
        self.agent = agent
    
    async def run(self):
        # Update respawn timer
        self.agent.update_respawn()
        
        current_pos = self.agent.position
        x, y = current_pos
        
        # Get PacMan's position for AI decisions
        pacman_pos = self.agent.blackboard.get_agent_position('pacman')
        
        logger.info(f"Ghost {self.agent.ghost_name} at {current_pos}, mode: {self.agent.ghost_mode}")
        
        # Check if power pellet is active to determine mode
        if self.agent.blackboard.is_power_pellet_active():
            if self.agent.ghost_mode != "frightened":
                self.agent.set_mode("frightened")
        else:
            if self.agent.ghost_mode == "frightened":
                self.agent.set_mode("normal")
        
        # Choose movement based on ghost mode
        if self.agent.ghost_mode == "returning":
            # Don't move while returning (ghost is temporarily out of play)
            logger.info(f"Ghost {self.agent.ghost_name} is returning, no movement")
            return
        elif self.agent.ghost_mode == "frightened":
            # Flee from PacMan
            new_pos = self._flee_from_pacman(current_pos, pacman_pos)
            logger.info(f"Ghost {self.agent.ghost_name} fleeing from PacMan")
        else:  # normal mode
            # Chase PacMan
            new_pos = self._chase_pacman(current_pos, pacman_pos)
            logger.info(f"Ghost {self.agent.ghost_name} chasing PacMan")
        
        # Update position if we got a valid move
        if new_pos and new_pos != current_pos:
            self.agent.position = new_pos
            self.agent.blackboard.update_agent_position(f"ghost_{self.agent.ghost_name}", new_pos)
            logger.info(f"Ghost {self.agent.ghost_name} moved to {new_pos}")
        else:
            logger.warning(f"Ghost {self.agent.ghost_name} couldn't move from {current_pos}")    
    def _chase_pacman(self, ghost_pos, pacman_pos):
        """Simple chase AI - move toward PacMan"""
        if not pacman_pos:
            return self._random_move(ghost_pos)
        
        gx, gy = ghost_pos
        px, py = pacman_pos
        
        # Calculate best direction toward PacMan
        dx = px - gx
        dy = py - gy
        
        # Prioritize horizontal or vertical movement
        possible_moves = []
        
        if dx > 0:  # PacMan is to the right
            possible_moves.append(('RIGHT', (gx + 1, gy)))
        elif dx < 0:  # PacMan is to the left
            possible_moves.append(('LEFT', (gx - 1, gy)))
        
        if dy > 0:  # PacMan is below
            possible_moves.append(('DOWN', (gx, gy + 1)))
        elif dy < 0:  # PacMan is above
            possible_moves.append(('UP', (gx, gy - 1)))
        
        # Filter valid moves
        valid_moves = []
        for direction, new_pos in possible_moves:
            if self.agent.maze.is_valid_position(new_pos[0], new_pos[1]):
                valid_moves.append(new_pos)
        
        if valid_moves:
            # Choose the move that gets closest to PacMan
            best_move = min(valid_moves, key=lambda pos: abs(pos[0] - px) + abs(pos[1] - py))
            return best_move
        
        # Fallback to random move if no direct path
        return self._random_move(ghost_pos)
    
    def _flee_from_pacman(self, ghost_pos, pacman_pos):
        """Flee AI - move away from PacMan"""
        if not pacman_pos:
            return self._random_move(ghost_pos)
        
        gx, gy = ghost_pos
        px, py = pacman_pos
        
        # Calculate direction away from PacMan
        dx = gx - px  # Opposite of chase logic
        dy = gy - py
        
        possible_moves = []
        
        if dx > 0:  # Move further right
            possible_moves.append(('RIGHT', (gx + 1, gy)))
        elif dx < 0:  # Move further left
            possible_moves.append(('LEFT', (gx - 1, gy)))
        
        if dy > 0:  # Move further down
            possible_moves.append(('DOWN', (gx, gy + 1)))
        elif dy < 0:  # Move further up
            possible_moves.append(('UP', (gx, gy - 1)))
        
        # If no clear flee direction, just move randomly
        if not possible_moves:
            return self._random_move(ghost_pos)
        
        # Filter valid moves
        valid_moves = []
        for direction, new_pos in possible_moves:
            if self.agent.maze.is_valid_position(new_pos[0], new_pos[1]):
                valid_moves.append(new_pos)
        
        if valid_moves:
            # Choose the move that gets furthest from PacMan
            best_move = max(valid_moves, key=lambda pos: abs(pos[0] - px) + abs(pos[1] - py))
            return best_move
        
        return self._random_move(ghost_pos)
    
    def _random_move(self, current_pos):
        """Fallback random movement"""
        x, y = current_pos
        valid_moves = self.agent.maze.get_valid_moves(x, y)
        
        if valid_moves:
            chosen_direction = random.choice(valid_moves)
            dx, dy = DIRECTIONS[chosen_direction]
            return (x + dx, y + dy)
        
        return current_pos
