import asyncio
import logging
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
from spade.template import Template
from communication.messages import (
    GameMessage, MessageType, PositionUpdateMessage, 
    StateQueryMessage, StateResponseMessage, GameEventMessage
)
from config.game_config import get_active_agent_jids

logger = logging.getLogger('PacManMAS.MessagingBehaviors')

class MessageReceiveBehaviour(CyclicBehaviour):
    """Continuously listen for and process incoming XMPP messages"""
    
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.coordinator = agent.coordinator
    
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            try:
                game_message = GameMessage.from_json(str(msg.body))
                
                logger.debug(f"Agent {self.agent.agent_name} received message: {game_message.type} from {game_message.sender}")
                
                # Process message through coordinator
                self.coordinator.process_incoming_message(game_message)
                
                # Handle specific message types that need responses
                if game_message.type == MessageType.STATE_QUERY:
                    await self._handle_state_query(game_message, msg.sender)
                
            except Exception as e:
                logger.error(f"Error processing received message: {e}")
                logger.debug(f"Message body was: {msg.body}")

    async def _handle_state_query(self, game_message, sender_jid):
        """Handle incoming state queries"""
        query_type = game_message.data['query_type']
        
        response_data = None
        
        if query_type == 'game_state':
            response_data = self.coordinator.get_game_state()
        elif query_type == 'agent_position':
            target_agent = game_message.data.get('target_agent')
            if target_agent:
                response_data = self.coordinator.get_agent_position(target_agent)
        elif query_type == 'all_positions':
            response_data = self.coordinator.get_all_positions()
        
        # Always send a response, even if None
        response_msg = StateResponseMessage(
            self.agent.agent_name,
            game_message.message_id,
            response_data
        )
        
        await self._send_message(response_msg, sender_jid)
        logger.debug(f"Sent state query response: {query_type} -> {response_data}")

    async def _send_message(self, game_message, recipient_jid):
        """Send a game message via XMPP"""
        msg = Message(to=str(recipient_jid))
        msg.body = game_message.to_json()
        await self.send(msg)

class PositionBroadcastBehaviour(PeriodicBehaviour):
    """Periodically broadcast agent position to all other agents"""
    
    def __init__(self, agent, period=0.1):  # Faster broadcast rate
        super().__init__(period=period)
        self.agent = agent
        self.coordinator = agent.coordinator
        self.last_position = None
    
    async def run(self):
        current_position = getattr(self.agent, 'position', None)
        
        # Always broadcast position, not just on change, for better synchronization
        if current_position:
            position_msg = PositionUpdateMessage(
                self.agent.agent_name,
                current_position,
                self._get_agent_type()
            )
            
            await self._broadcast_message(position_msg)
            # self.coordinator.update_local_position(current_position)
            self.last_position = current_position
            
            logger.debug(f"Agent {self.agent.agent_name} broadcasted position: {current_position}")
    
    def _get_agent_type(self):
        """Get agent type for message metadata"""
        if hasattr(self.agent, 'ghost_name'):
            return f"ghost_{self.agent.ghost_name}"
        elif 'pacman' in self.agent.agent_name:
            return 'pacman'
        elif 'environment' in self.agent.agent_name:
            return 'environment'
        return 'agent'
    
    async def _broadcast_message(self, game_message):
        """Broadcast message to all known ACTIVE agents."""
        active_jids = get_active_agent_jids()
        for jid_str in active_jids:
            if jid_str != str(self.agent.jid):  # Don't send to self
                msg = Message(to=jid_str)
                msg.body = game_message.to_json()
                await self.send(msg)

class GameEventBroadcastBehaviour:
    """Mixin behavior for broadcasting game events"""
    
    async def broadcast_game_event(self, event_type, position=None, points=0, extra_data=None):
        """Broadcast a game event to all agents"""
        event_msg = GameEventMessage(
            self.agent.agent_name,
            event_type,
            position,
            points,
            extra_data
        )
        
        await self._broadcast_message_mixin(event_msg)
        logger.info(f"Broadcasted game event: {event_type} (+{points} points)")

    async def _broadcast_message_mixin(self, game_message): # Renamed to avoid conflict if the class using it also has _broadcast_message
        """Broadcast message to all known ACTIVE agents (for mixin)."""
        # This method relies on `self.agent` and `self.send()` being available in the class that uses this mixin.
        active_jids = get_active_agent_jids()
        for jid_str in active_jids:
            if jid_str != str(self.agent.jid):
                msg = Message(to=jid_str)
                msg.body = game_message.to_json()
                await self.send(msg) # self.send must be available from the agent class

    
    async def _broadcast_message(self, game_message):
        """Broadcast message to all known agents"""
        all_jids = [
            'pacman@localhost',
            'environment@localhost',
            'blinky@localhost', 
            'pinky@localhost',
            'inky@localhost',
            'clyde@localhost'
        ]
        
        for jid in all_jids:
            if jid != str(self.agent.jid):
                msg = Message(to=jid)
                msg.body = game_message.to_json()
                await self.send(msg)

class StateQueryBehaviour:
    """Mixin behavior for querying game state from other agents"""
    
    async def query_agent_position(self, target_agent, timeout=1.0):
        """Query specific agent position from environment"""
        query_msg = StateQueryMessage(
            self.agent.agent_name,
            'agent_position',
            target_agent
        )
        
        return await self._send_query('environment@localhost', query_msg, timeout)
    
    async def query_all_positions(self, timeout=1.0):
        """Query all agent positions from environment"""
        query_msg = StateQueryMessage(
            self.agent.agent_name,
            'all_positions'
        )
        
        return await self._send_query('environment@localhost', query_msg, timeout)
    
    async def query_game_state(self, timeout=1.0):
        """Query current game state from environment"""
        query_msg = StateQueryMessage(
            self.agent.agent_name,
            'game_state'
        )
        
        return await self._send_query('environment@localhost', query_msg, timeout)
    
    async def _send_query(self, recipient_jid, query_msg, timeout):
        """Send query and wait for response"""
        # Create future for response
        future = await self.agent.coordinator.create_query_future(query_msg.message_id)
        
        # Send query message
        msg = Message(to=recipient_jid)
        msg.body = query_msg.to_json()
        await self.send(msg)
        
        # Wait for response with timeout
        try:
            response = await asyncio.wait_for(future, timeout=timeout)
            logger.debug(f"Query response received: {query_msg.data['query_type']}")
            return response
        except asyncio.TimeoutError:
            logger.warning(f"Query timeout: {query_msg.data['query_type']} to {recipient_jid}")
            return None
