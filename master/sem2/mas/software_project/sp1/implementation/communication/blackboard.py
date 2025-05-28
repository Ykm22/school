import logging
import threading
import time

logger = logging.getLogger('PacManMAS.Blackboard')

class Blackboard:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.agent_positions = {}
        self.consumed_ghosts = {}
        self.frightened_ghosts = {}
        self.game_state = {
            'step': 0,
            'score': 0,
            'running': True,
            'power_pellet_active': False,
            'power_pellet_end_time': 0,
            'dots_collected': 0,
            'power_pellets_collected': 0,
            'game_complete': False,
            'game_over': False,
            'ghosts_eaten': 0
        }
        self._data_lock = threading.Lock()
        self._initialized = True
        logger.info("Blackboard initialized")
    
    def update_agent_position(self, agent_name, position):
        with self._data_lock:
            self.agent_positions[agent_name] = position
            logger.debug(f"Agent {agent_name} position updated to {position}")
    
    def get_agent_position(self, agent_name):
        with self._data_lock:
            return self.agent_positions.get(agent_name)
    
    def get_all_positions(self):
        with self._data_lock:
            return self.agent_positions.copy()
    
    def update_game_state(self, key, value):
        with self._data_lock:
            self.game_state[key] = value
            logger.debug(f"Game state updated: {key} = {value}")
    
    def get_game_state(self):
        with self._data_lock:
            return self.game_state.copy()
    
    def increment_step(self):
        with self._data_lock:
            self.game_state['step'] += 1
    
    def add_score(self, points):
        with self._data_lock:
            self.game_state['score'] += points
            logger.info(f"Score increased by {points}. Total score: {self.game_state['score']}")
    
    def collect_dot(self):
        with self._data_lock:
            self.game_state['dots_collected'] += 1
            self.game_state['score'] += 10  # 10 points per dot
            logger.info(f"Dot collected! Total dots: {self.game_state['dots_collected']}, Score: {self.game_state['score']}")
    
    def collect_power_pellet(self):
        with self._data_lock:
            self.game_state['power_pellets_collected'] += 1
            self.game_state['power_pellet_active'] = True
            self.game_state['power_pellet_end_time'] = time.time() + 8.0  # 8 seconds duration
            self.game_state['score'] += 50  # 50 points per power pellet
            self.game_state['ghosts_eaten'] = 0  # Reset ghost eating counter
            logger.info(f"Power pellet collected! Power mode activated for 8 seconds. Score: {self.game_state['score']}")
    
    def check_power_pellet_status(self):
        with self._data_lock:
            if self.game_state['power_pellet_active']:
                if time.time() >= self.game_state['power_pellet_end_time']:
                    self.game_state['power_pellet_active'] = False
                    logger.info("Power pellet effect ended")
                    return False
                return True
            return False
    
    def is_power_pellet_active(self):
        with self._data_lock:
            return self.game_state['power_pellet_active']
    
    def set_game_complete(self):
        with self._data_lock:
            self.game_state['game_complete'] = True
            self.game_state['running'] = False
            logger.info("Game completed! All collectibles gathered!")
    
    def eat_ghost(self, ghost_name):
        with self._data_lock:
            self.game_state['ghosts_eaten'] += 1
            points = 200 * (2 ** (self.game_state['ghosts_eaten'] - 1))  # Increasing points
            self.game_state['score'] += points
            logger.info(f"Ghost {ghost_name} eaten! +{points} points! Total ghosts eaten this power pellet: {self.game_state['ghosts_eaten']}")
            return points

    def set_ghost_consumed(self, ghost_name):
        with self._data_lock:
            self.consumed_ghosts[ghost_name] = True
            logger.info(f"Ghost {ghost_name} marked as consumed")

    def is_ghost_consumed(self, ghost_name):
        with self._data_lock:
            return self.consumed_ghosts.get(ghost_name, False)

    def clear_ghost_consumed(self, ghost_name):
        with self._data_lock:
            if ghost_name in self.consumed_ghosts:
                del self.consumed_ghosts[ghost_name]
    
    def set_ghost_frightened(self, ghost_name):
        with self._data_lock:
            self.frightened_ghosts[ghost_name] = True
            logger.info(f"Ghost {ghost_name} marked as frightened")

    def is_ghost_frightened(self, ghost_name):
        with self._data_lock:
            return self.frightened_ghosts.get(ghost_name, False)

    def clear_ghost_frightened(self, ghost_name):
        with self._data_lock:
            if ghost_name in self.frightened_ghosts:
                del self.frightened_ghosts[ghost_name]

    def set_game_over(self):
        with self._data_lock:
            self.game_state['game_over'] = True
            self.game_state['running'] = False
            logger.info("Game Over! PacMan was caught!")
