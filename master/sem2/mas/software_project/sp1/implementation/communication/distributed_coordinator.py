import asyncio
import logging
import time
import threading
from typing import Dict, List, Optional
from communication.messages import GameMessage, MessageType

logger = logging.getLogger('PacManMAS.DistributedCoordinator')

class DistributedGameCoordinator:
    """
    Manages distributed game state without a centralized blackboard.
    Each agent maintains local cache and communicates via XMPP.
    """
    
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.local_cache = {
            'agent_positions': {},
            'game_state': {
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
            },
            'last_updated': {},
            'pending_queries': {},
            'frightened_ghosts': set(),
            'consumed_ghosts': set()
        }
        self._cache_lock = threading.RLock()
        self._message_queue = asyncio.Queue()
        self._response_futures = {}
        
    def update_local_position(self, position):
        """Update own position in local cache"""
        with self._cache_lock:
            self.local_cache['agent_positions'][self.agent_name] = tuple(position)
            self.local_cache['last_updated'][self.agent_name] = time.time()
    
    def process_incoming_message(self, message: GameMessage):
        """Process received message and update local cache"""
        with self._cache_lock:
            # Convert string type to MessageType enum if needed
            msg_type = message.type
            if isinstance(msg_type, str):
                try:
                    msg_type = MessageType(msg_type)
                except ValueError:
                    logger.warning(f"Unknown message type: {msg_type}")
                    return
            
            if msg_type == MessageType.POSITION_UPDATE:
                self._handle_position_update(message)
            elif msg_type == MessageType.GAME_EVENT:
                self._handle_game_event(message)
            elif msg_type == MessageType.STATE_RESPONSE:
                self._handle_state_response(message)
            elif msg_type == MessageType.POWER_MODE_CHANGED:
                self._handle_power_mode_change(message)
            elif msg_type == MessageType.STATE_QUERY:
                # Will be handled by specific agent behaviors
                pass
    
    def _handle_position_update(self, message: GameMessage):
        """Handle position update from another agent"""
        agent_name = message.sender
        position = tuple(message.data['position'])
        agent_type = message.data.get('agent_type', 'agent')
        
        # Map agent types to position keys
        if agent_type.startswith('ghost_'):
            position_key = f"ghost_{agent_name}"
        else:
            position_key = agent_name
        
        self.local_cache['agent_positions'][position_key] = position
        self.local_cache['last_updated'][position_key] = message.timestamp
        
        logger.debug(f"Updated position cache: {position_key} -> {position}")
    
    def _handle_game_event(self, message: GameMessage):
        """Handle game events (dots collected, etc.)"""
        event_type = message.data['event_type']
        points = message.data.get('points', 0)
        
        if event_type == 'dot_collected':
            self.local_cache['game_state']['dots_collected'] += 1
            self.local_cache['game_state']['score'] += points
        elif event_type == 'power_pellet_collected':
            self.local_cache['game_state']['power_pellets_collected'] += 1
            self.local_cache['game_state']['score'] += points
            self.local_cache['game_state']['power_pellet_active'] = True
            self.local_cache['game_state']['power_pellet_end_time'] = time.time() + 8.0
            self.local_cache['game_state']['ghosts_eaten'] = 0
            # Set all ghosts as frightened
            self.local_cache['frightened_ghosts'] = {'blinky', 'pinky', 'inky', 'clyde'}
        elif event_type == 'ghost_eaten':
            ghost_name = message.data.get('extra_data', {}).get('ghost_name')
            self.local_cache['game_state']['ghosts_eaten'] += 1
            self.local_cache['game_state']['score'] += points
            if ghost_name:
                self.local_cache['consumed_ghosts'].add(ghost_name)
        elif event_type == 'game_complete':
            self.local_cache['game_state']['game_complete'] = True
            self.local_cache['game_state']['running'] = False
        elif event_type == 'game_over':
            self.local_cache['game_state']['game_over'] = True
            self.local_cache['game_state']['running'] = False
        
        logger.info(f"Processed game event: {event_type}, Score: {self.local_cache['game_state']['score']}")
    
    def _handle_state_response(self, message: GameMessage):
        """Handle response to state query"""
        query_id = message.data['query_id']
        response_data = message.data['response_data']
        
        if query_id in self._response_futures:
            future = self._response_futures[query_id]
            if not future.done():
                future.set_result(response_data)
            del self._response_futures[query_id]
    
    def _handle_power_mode_change(self, message: GameMessage):
        """Handle power mode activation/deactivation"""
        active = message.data['active']
        
        self.local_cache['game_state']['power_pellet_active'] = active
        
        if active:
            duration = message.data.get('duration', 8.0)
            self.local_cache['game_state']['power_pellet_end_time'] = time.time() + duration
            self.local_cache['frightened_ghosts'] = {'blinky', 'pinky', 'inky', 'clyde'}
            logger.info("Power mode activated - all ghosts frightened!")
        else:
            self.local_cache['frightened_ghosts'].clear()
            logger.info("Power mode deactivated - ghosts return to normal")
    
    def get_agent_position(self, agent_name, max_age=2.0):
        """Get cached position of an agent (returns None if too old)"""
        with self._cache_lock:
            if agent_name in self.local_cache['agent_positions']:
                last_update = self.local_cache['last_updated'].get(agent_name, 0)
                if time.time() - last_update <= max_age:
                    return self.local_cache['agent_positions'][agent_name]
        return None
    
    def get_all_positions(self, max_age=2.0):
        """Get all cached positions that aren't too old"""
        positions = {}
        current_time = time.time()
        
        with self._cache_lock:
            for agent_name, position in self.local_cache['agent_positions'].items():
                last_update = self.local_cache['last_updated'].get(agent_name, 0)
                if current_time - last_update <= max_age:
                    positions[agent_name] = position
        
        return positions
    
    def get_game_state(self):
        """Get current cached game state"""
        with self._cache_lock:
            # Update power pellet status
            if self.local_cache['game_state']['power_pellet_active']:
                if time.time() >= self.local_cache['game_state']['power_pellet_end_time']:
                    self.local_cache['game_state']['power_pellet_active'] = False
                    self.local_cache['frightened_ghosts'].clear()
            
            return self.local_cache['game_state'].copy()
    
    def is_ghost_frightened(self, ghost_name):
        """Check if a ghost is currently frightened"""
        with self._cache_lock:
            return ghost_name in self.local_cache['frightened_ghosts']
    
    def is_ghost_consumed(self, ghost_name):
        """Check if a ghost was recently consumed"""
        with self._cache_lock:
            return ghost_name in self.local_cache['consumed_ghosts']
    
    def clear_ghost_consumed(self, ghost_name):
        """Clear consumed status for a ghost"""
        with self._cache_lock:
            self.local_cache['consumed_ghosts'].discard(ghost_name)
    
    def increment_step(self):
        """Increment local step counter"""
        with self._cache_lock:
            self.local_cache['game_state']['step'] += 1
    
    async def create_query_future(self, query_id):
        """Create a future for waiting on query response"""
        future = asyncio.Future()
        self._response_futures[query_id] = future
        return future
    
    def get_cache_info(self):
        """Get diagnostic information about cache state"""
        with self._cache_lock:
            current_time = time.time()
            cache_info = {
                'positions_count': len(self.local_cache['agent_positions']),
                'step': self.local_cache['game_state']['step'],
                'score': self.local_cache['game_state']['score'],
                'stale_positions': []
            }
            
            for agent_name, last_update in self.local_cache['last_updated'].items():
                age = current_time - last_update
                if age > 2.0:
                    cache_info['stale_positions'].append((agent_name, age))
            
            return cache_info
