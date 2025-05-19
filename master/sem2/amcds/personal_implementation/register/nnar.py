from pb import communication_protocol_pb2 as pb
from util.log import debug, error, info

class NnAtomicRegister:
    """
    (N,N) Atomic Register abstraction.
    Implements the Read-Impose Write-Consult-Majority algorithm from the textbook.
    """
    
    def __init__(self, message_queue, n, key, writer_rank):
        """
        Initialize a new (N,N) Atomic Register.
        
        Parameters:
            message_queue (list): Shared message queue
            n (int): Number of processes
            key (str): Register identifier
            writer_rank (int): Rank of this process
        """
        self.message_queue = message_queue
        self.n = n
        self.key = key
        
        # Algorithm state
        self.timestamp = 0
        self.writer_rank = writer_rank
        self.value = -1  # -1 represents undefined
        
        self.acks = 0
        self.write_val = None
        self.read_id = 0
        self.read_list = {}  # Map of process port to received value
        self.reading = False
    
    def handle(self, message):
        """
        Handle an incoming message.
        
        Parameters:
            message (Message): The message to handle
            
        Returns:
            bool: True if handled successfully, False otherwise
        """
        abstraction_id = f"app.nnar[{self.key}]"
        msg_to_send = None
        
        if message.type == pb.Message.BEB_DELIVER:
            # Handle BEB delivery
            inner_message = message.bebDeliver.message
            
            if inner_message.type == pb.Message.NNAR_INTERNAL_READ:
                # Someone wants to read our value
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.PL_SEND
                msg_to_send.systemId = message.systemId
                msg_to_send.FromAbstractionId = abstraction_id
                msg_to_send.ToAbstractionId = f"{abstraction_id}.pl"
                
                # Set destination and inner message
                msg_to_send.plSend.destination.CopyFrom(message.bebDeliver.sender)
                
                # Create NNAR_INTERNAL_VALUE message
                value_msg = pb.Message()
                value_msg.type = pb.Message.NNAR_INTERNAL_VALUE
                value_msg.FromAbstractionId = abstraction_id
                value_msg.ToAbstractionId = abstraction_id
                
                # Set value info
                value_msg.nnarInternalValue.readId = inner_message.nnarInternalRead.readId
                value_msg.nnarInternalValue.timestamp = self.timestamp
                value_msg.nnarInternalValue.writerRank = self.writer_rank
                
                # Set value
                value_msg.nnarInternalValue.value.defined = (self.value != -1)
                if self.value != -1:
                    value_msg.nnarInternalValue.value.v = self.value
                
                msg_to_send.plSend.message.CopyFrom(value_msg)
                
            elif inner_message.type == pb.Message.NNAR_INTERNAL_WRITE:
                # Someone wants to write a value
                write_msg = inner_message.nnarInternalWrite
                
                # Compare timestamps and update if needed
                if (write_msg.timestamp > self.timestamp or 
                    (write_msg.timestamp == self.timestamp and 
                     write_msg.writerRank > self.writer_rank)):
                    self.timestamp = write_msg.timestamp
                    self.writer_rank = write_msg.writerRank
                    
                    # Update value
                    if write_msg.value.defined:
                        self.value = write_msg.value.v
                    else:
                        self.value = -1
                
                # Send ACK
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.PL_SEND
                msg_to_send.systemId = message.systemId
                msg_to_send.FromAbstractionId = abstraction_id
                msg_to_send.ToAbstractionId = f"{abstraction_id}.pl"
                
                # Set destination and inner message
                msg_to_send.plSend.destination.CopyFrom(message.bebDeliver.sender)
                
                # Create NNAR_INTERNAL_ACK message
                ack_msg = pb.Message()
                ack_msg.type = pb.Message.NNAR_INTERNAL_ACK
                ack_msg.FromAbstractionId = abstraction_id
                ack_msg.ToAbstractionId = abstraction_id
                ack_msg.nnarInternalAck.readId = self.read_id
                
                msg_to_send.plSend.message.CopyFrom(ack_msg)
        
        elif message.type == pb.Message.NNAR_WRITE:
            # Handle write request
            self.read_id += 1
            self.write_val = message.nnarWrite.value
            self.acks = 0
            self.read_list = {}
            
            # Broadcast internal read
            msg_to_send = pb.Message()
            msg_to_send.type = pb.Message.BEB_BROADCAST
            msg_to_send.systemId = message.systemId
            msg_to_send.FromAbstractionId = abstraction_id
            msg_to_send.ToAbstractionId = f"{abstraction_id}.beb"
            
            # Create NNAR_INTERNAL_READ message
            read_msg = pb.Message()
            read_msg.type = pb.Message.NNAR_INTERNAL_READ
            read_msg.FromAbstractionId = abstraction_id
            read_msg.ToAbstractionId = abstraction_id
            read_msg.nnarInternalRead.readId = self.read_id
            
            msg_to_send.bebBroadcast.message.CopyFrom(read_msg)
            
        elif message.type == pb.Message.NNAR_READ:
            # Handle read request
            self.read_id += 1
            self.acks = 0
            self.read_list = {}
            self.reading = True
            
            # Broadcast internal read
            msg_to_send = pb.Message()
            msg_to_send.type = pb.Message.BEB_BROADCAST
            msg_to_send.systemId = message.systemId
            msg_to_send.FromAbstractionId = abstraction_id
            msg_to_send.ToAbstractionId = f"{abstraction_id}.beb"
            
            # Create NNAR_INTERNAL_READ message
            read_msg = pb.Message()
            read_msg.type = pb.Message.NNAR_INTERNAL_READ
            read_msg.FromAbstractionId = abstraction_id
            read_msg.ToAbstractionId = abstraction_id
            read_msg.nnarInternalRead.readId = self.read_id
            
            msg_to_send.bebBroadcast.message.CopyFrom(read_msg)
            
        elif message.type == pb.Message.PL_DELIVER:
            # Handle PL delivery
            inner_message = message.plDeliver.message
            
            if inner_message.type == pb.Message.NNAR_INTERNAL_VALUE:
                # Received value from a process
                value_msg = inner_message.nnarInternalValue
