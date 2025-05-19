from pb import communication_protocol_pb2 as pb
from util.log import debug, error

class BestEffortBroadcast:
    """
    Best Effort Broadcast abstraction.
    Implements the basic broadcast abstraction from the textbook.
    """
    
    def __init__(self, message_queue, processes, abstraction_id):
        """
        Initialize a new Best Effort Broadcast.
        
        Parameters:
            message_queue (list): Shared message queue
            processes (list): List of ProcessId instances
            abstraction_id (str): Abstraction ID for this instance
        """
        self.message_queue = message_queue
        self.processes = processes
        self.id = abstraction_id
    
    def handle(self, message):
        """
        Handle an incoming message.
        
        Parameters:
            message (Message): The message to handle
            
        Returns:
            bool: True if handled successfully, False otherwise
        """
        if message.type == pb.Message.BEB_BROADCAST:
            # Handle broadcast request - send to all processes
            for process in self.processes:
                # Create PL_SEND message for each process
                pl_send = pb.Message()
                pl_send.type = pb.Message.PL_SEND
                pl_send.systemId = message.systemId
                pl_send.FromAbstractionId = self.id
                pl_send.ToAbstractionId = f"{self.id}.pl"
                
                # Set destination and inner message
                pl_send.plSend.destination.CopyFrom(process)
                pl_send.plSend.message.CopyFrom(message.bebBroadcast.message)
                
                # Add to message queue
                self.message_queue.append(pl_send)
            
            return True
            
        elif message.type == pb.Message.PL_DELIVER:
            # Handle delivery from perfect link
            # Create BEB_DELIVER message
            beb_deliver = pb.Message()
            beb_deliver.type = pb.Message.BEB_DELIVER
            beb_deliver.systemId = message.systemId
            beb_deliver.FromAbstractionId = self.id
            beb_deliver.ToAbstractionId = message.plDeliver.message.ToAbstractionId
            
            # Set sender and inner message
            beb_deliver.bebDeliver.sender.CopyFrom(message.plDeliver.sender)
            beb_deliver.bebDeliver.message.CopyFrom(message.plDeliver.message)
            
            # Add to message queue
            self.message_queue.append(beb_deliver)
            return True
            
        else:
            error(f"BestEffortBroadcast cannot handle message type {message.type}")
            return False
    
    def destroy(self):
        """Clean up resources"""
        # No resources to clean up
        pass
