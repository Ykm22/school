import json
import time
from enum import Enum

class MessageType(Enum):
    POSITION_UPDATE = "position_update"
    GAME_EVENT = "game_event"
    STATE_QUERY = "state_query"
    STATE_RESPONSE = "state_response"
    POWER_MODE_CHANGED = "power_mode_changed"
    COLLISION_DETECTED = "collision_detected"
    GAME_STEP_SYNC = "game_step_sync"
    AGENT_READY = "agent_ready"

class GameMessage:
    def __init__(self, msg_type, sender, data=None, recipient=None):
        self.type = msg_type
        self.sender = sender
        self.data = data or {}
        self.recipient = recipient
        self.timestamp = time.time()
        self.message_id = f"{sender}_{int(self.timestamp * 1000)}"
    
    def to_json(self):
        return json.dumps({
            'type': self.type.value if isinstance(self.type, MessageType) else self.type,
            'sender': self.sender,
            'data': self.data,
            'recipient': self.recipient,
            'timestamp': self.timestamp,
            'message_id': self.message_id
        })
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        msg = cls(
            msg_type=data['type'],
            sender=data['sender'],
            data=data.get('data', {}),
            recipient=data.get('recipient')
        )
        msg.timestamp = data['timestamp']
        msg.message_id = data['message_id']
        return msg

class PositionUpdateMessage(GameMessage):
    def __init__(self, sender, position, agent_type="agent"):
        super().__init__(
            MessageType.POSITION_UPDATE,
            sender,
            {
                'position': position,
                'agent_type': agent_type
            }
        )

class GameEventMessage(GameMessage):
    def __init__(self, sender, event_type, position=None, points=0, extra_data=None):
        data = {
            'event_type': event_type,  # 'dot_collected', 'power_pellet_collected', 'ghost_eaten'
            'points': points
        }
        if position:
            data['position'] = position
        if extra_data:
            data.update(extra_data)
        
        super().__init__(MessageType.GAME_EVENT, sender, data)

class StateQueryMessage(GameMessage):
    def __init__(self, sender, query_type, target_agent=None):
        super().__init__(
            MessageType.STATE_QUERY,
            sender,
            {
                'query_type': query_type,  # 'game_state', 'agent_position', 'all_positions'
                'target_agent': target_agent
            }
        )

class StateResponseMessage(GameMessage):
    def __init__(self, sender, query_id, response_data):
        super().__init__(
            MessageType.STATE_RESPONSE,
            sender,
            {
                'query_id': query_id,
                'response_data': response_data
            }
        )

class PowerModeMessage(GameMessage):
    def __init__(self, sender, active, duration=0):
        super().__init__(
            MessageType.POWER_MODE_CHANGED,
            sender,
            {
                'active': active,
                'duration': duration
            }
        )

class GameStepSyncMessage(GameMessage):
    def __init__(self, sender, step_number, action="step_start"):
        super().__init__(
            MessageType.GAME_STEP_SYNC,
            sender,
            {
                'step_number': step_number,
                'action': action  # 'step_start', 'step_complete', 'ready_for_next'
            }
        )
