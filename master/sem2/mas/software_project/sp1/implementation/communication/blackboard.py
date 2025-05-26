import logging
import threading

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
        self.game_state = {
            'step': 0,
            'score': 0,
            'running': True
        }
        self._data_lock = threading.Lock()
        self._initialized = True
        logger.info("Blackboard initialized")
    
    def update_agent_position(self, agent_name, position):
        with self._data_lock:
            self.agent_positions[agent_name] = position
            logger.info(f"Agent {agent_name} position updated to {position}")
    
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
            logger.info(f"Game step incremented to {self.game_state['step']}")
