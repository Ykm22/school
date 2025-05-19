import socket
import struct
from pb import communication_protocol_pb2 as pb
from util.log import debug, error

class PerfectLink:
    """
    Perfect Link abstraction.
    Handles sending and receiving messages over TCP.
    """
    
    def __init__(self, host, port, hub_address, system_id, processes, parent_id=None):
        """
        Initialize a new Perfect Link.
        
        Parameters:
            host (str): Host address
            port (int): Port number
            hub_address (str): Hub address (host:port)
            system_id (str): System ID
            processes (list): List of ProcessId instances
            parent_id (str, optional): Parent abstraction ID
        """
        self.host = host
        self.port = port
        self.hub_address = hub_address
        self.system_id = system_id
        self.processes = processes
        self.parent_id = parent_id
        self.message_queue = []
    
    def copy_with_parent(self, parent_id):
        """
        Create a new PerfectLink with a different parent ID.
        
        Parameters:
            parent_id (str): New parent abstraction ID
            
        Returns:
            PerfectLink: A new instance with the same properties but different parent ID
        """
        return PerfectLink(
            self.host,
            self.port,
            self.hub_address,
            self.system_id,
            self.processes,
            parent_id
        )
    
    def handle(self, message):
        """
        Handle an incoming message.
        
        Parameters:
            message (Message): The message to handle
            
        Returns:
            bool: True if handled successfully, False otherwise
        """
        if message.type == pb.Message.NETWORK_MESSAGE:
            # Handle network message
            sender = None
            for p in self.processes:
                if (p.host == message.networkMessage.senderHost and 
                    p.port == message.networkMessage.senderListeningPort):
                    sender = p
                    break
            
            # Create PL_DELIVER message
            pl_deliver = pb.Message()
            pl_deliver.type = pb.Message.PL_DELIVER
            pl_deliver.systemId = self.system_id
            pl_deliver.FromAbstractionId = message.ToAbstractionId
            pl_deliver.ToAbstractionId = self.parent_id if self.parent_id else "app"
            
            # Set sender and inner message
            pl_deliver.plDeliver.sender.CopyFrom(sender)
            pl_deliver.plDeliver.message.CopyFrom(message.networkMessage.message)
            
            # Add to message queue
            self.message_queue.append(pl_deliver)
            return True
            
        elif message.type == pb.Message.PL_SEND:
            # Handle PL_SEND message
            return self.send(message)
            
        else:
            error(f"PerfectLink cannot handle message type {message.type}")
            return False
    
    def send(self, message):
        """
        Send a message.
        
        Parameters:
            message (Message): PL_SEND message to send
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create network message
            network_message = pb.Message()
            network_message.type = pb.Message.NETWORK_MESSAGE
            network_message.systemId = self.system_id
            network_message.ToAbstractionId = message.ToAbstractionId
            
            # Set sender info
            network_message.networkMessage.senderHost = self.host
            network_message.networkMessage.senderListeningPort = self.port
            
            # Copy the inner message
            network_message.networkMessage.message.CopyFrom(message.plSend.message)
            
            # Serialize message
            data = network_message.SerializeToString()
            
            # Get destination address
            if message.plSend.destination:
                dest_host = message.plSend.destination.host
                dest_port = message.plSend.destination.port
            else:
                # Default to hub
                hub_host, hub_port_str = self.hub_address.split(':')
                dest_host = hub_host
                dest_port = int(hub_port_str)
            
            # Send message
            self._send_tcp_message(dest_host, dest_port, data)
            return True
            
        except Exception as e:
            error(f"Error sending message: {e}")
            return False
    
    def _send_tcp_message(self, host, port, data):
        """
        Send a TCP message.
        
        Parameters:
            host (str): Destination host
            port (int): Destination port
            data (bytes): Message data
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                
                # Send message size (4 bytes) followed by message data
                size = len(data)
                size_bytes = struct.pack('>I', size)  # 4 bytes, big-endian
                
                s.sendall(size_bytes + data)
                
        except Exception as e:
            error(f"TCP send error to {host}:{port}: {e}")
    
    def parse(self, data):
        """
        Parse received data into a Message.
        
        Parameters:
            data (bytes): Raw message data
            
        Returns:
            Message: Parsed message
        """
        try:
            message = pb.Message()
            message.ParseFromString(data)
            return message
        except Exception as e:
            error(f"Error parsing message: {e}")
            return None
    
    def destroy(self):
        """Clean up resources"""
        # No resources to clean up
        pass
