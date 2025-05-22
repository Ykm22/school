import queue
import pb.communication_protocol_pb2 as pb

class NNAtomicRegister():
    def __init__(self, msg_queue: queue.Queue, n: int, abstraction_id: str, timestamp: int, writer_rank, value, read_list):
        self.msg_queue = msg_queue
        self.n = n
        self.abstraction_id = abstraction_id
        self.timestamp = timestamp
        self.writer_rank = writer_rank
        self.value = value
        self.read_list = read_list

        self.acks = 0
        self.write_value = pb.Value()
        self.read_id = 0
        self.reading = False

    def handle(self, msg: pb.Message):
        msg_to_send = None
        match msg.type:
            case pb.Message.Type.NNAR_WRITE:
                # print(msg)
                self.read_id = self.read_id + 1
                self.write_value.CopyFrom(msg.nnarWrite.value)
                self.acks = 0
                self.read_list = {}  # Empty dictionary for new read operation

                # Create broadcast message for internal read
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.Type.BEB_BROADCAST
                msg_to_send.FromAbstractionId = self.abstraction_id
                msg_to_send.ToAbstractionId = f"{self.abstraction_id}.beb"

                # Create the inner message for BEB broadcast
                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.NNAR_INTERNAL_READ
                inner_message.FromAbstractionId = self.abstraction_id
                inner_message.ToAbstractionId = self.abstraction_id
                inner_message.nnarInternalRead.readId = self.read_id

                # Attach the inner message to the broadcast
                msg_to_send.bebBroadcast.message.CopyFrom(inner_message)

            case pb.Message.Type.NNAR_READ:
                self.read_id = self.read_id + 1
                self.acks = 0
                self.read_list = {}
                self.reading = True

                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.Type.BEB_BROADCAST
                msg_to_send.FromAbstractionId = self.abstraction_id
                msg_to_send.ToAbstractionId = self.abstraction_id + ".beb"

                # Create inner message for BEB broadcast
                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.NNAR_INTERNAL_READ
                inner_message.FromAbstractionId = self.abstraction_id
                inner_message.ToAbstractionId = self.abstraction_id
                inner_message.nnarInternalRead.readId = self.read_id

                # Attach the inner message to the broadcast
                msg_to_send.bebBroadcast.message.CopyFrom(inner_message)
            
            case pb.Message.Type.BEB_DELIVER:
                match msg.bebDeliver.message.type:
                    case pb.Message.Type.NNAR_INTERNAL_READ:
                        # Create message for PL_SEND
                        msg_to_send = pb.Message()
                        msg_to_send.type = pb.Message.Type.PL_SEND
                        msg_to_send.FromAbstractionId = self.abstraction_id
                        msg_to_send.ToAbstractionId = f"{self.abstraction_id}.pl"

                        inner_message = pb.Message()
                        inner_message.type = pb.Message.Type.NNAR_INTERNAL_VALUE
                        inner_message.FromAbstractionId = self.abstraction_id
                        inner_message.ToAbstractionId = self.abstraction_id

                        internal_value = self._build_nnar_internal_value()
                        inner_message.nnarInternalValue.CopyFrom(internal_value)

                        msg_to_send.plSend.destination.CopyFrom(msg.bebDeliver.sender)
                        msg_to_send.plSend.message.CopyFrom(inner_message)
                    case pb.Message.Type.NNAR_INTERNAL_WRITE:
                        # Get internal write message from the delivered message
                        w_msg = msg.bebDeliver.message.nnarInternalWrite

                        # Create value objects for comparison
                        v_incoming = pb.NnarInternalValue()
                        v_incoming.timestamp = w_msg.timestamp
                        v_incoming.writerRank = w_msg.writerRank

                        v_current = pb.NnarInternalValue()
                        v_current.timestamp = self.timestamp
                        v_current.writerRank = self.writer_rank

                        # Compare and update if incoming value is higher
                        if self._compare(v_incoming, v_current) == 1:
                            self.timestamp = w_msg.timestamp
                            self.writer_rank = w_msg.writerRank
                            self._update_value(w_msg.value)

                        # Create acknowledgment message
                        msg_to_send = pb.Message()
                        msg_to_send.type = pb.Message.Type.PL_SEND
                        msg_to_send.FromAbstractionId = self.abstraction_id
                        msg_to_send.ToAbstractionId = f"{self.abstraction_id}.pl"

                        # Set destination
                        msg_to_send.plSend.destination.CopyFrom(msg.bebDeliver.sender)

                        # Create inner acknowledgment message
                        inner_message = pb.Message()
                        inner_message.type = pb.Message.Type.NNAR_INTERNAL_ACK
                        inner_message.FromAbstractionId = self.abstraction_id
                        inner_message.ToAbstractionId = self.abstraction_id
                        inner_message.nnarInternalAck.readId = self.read_id

                        # Assign inner message to outer message
                        msg_to_send.plSend.message.CopyFrom(inner_message)
            case pb.Message.Type.PL_DELIVER:
                # print("\n\n\nim here\n\n")
                match msg.plDeliver.message.type:
                    case pb.Message.NNAR_INTERNAL_VALUE:
                        # Get internal value message from the delivered message
                        v_msg = msg.plDeliver.message.nnarInternalValue

                        if v_msg.readId == self.read_id:
                            # Store the message in the read list using sender's port as key
                            self.read_list[msg.plDeliver.sender.port] = v_msg
                            
                            # Set the writer rank based on the sender
                            # Note: In Python we might need to create a copy of v_msg first
                            # Since modifying directly might not work as expected with protobufs
                            copied_msg = pb.NnarInternalValue()
                            copied_msg.CopyFrom(v_msg)
                            copied_msg.writerRank = msg.plDeliver.sender.rank
                            self.read_list[msg.plDeliver.sender.port] = copied_msg
                            
                            # Check if we have majority responses
                            if len(self.read_list) > self.n // 2:
                                # Get highest timestamp/rank message
                                h = self._highest()                                  
                                self.read_list = {}
                                
                                # If not in reading mode, prepare for write
                                if not self.reading:
                                    h.timestamp = h.timestamp + 1
                                    h.writerRank = self.writer_rank
                                    # Copy the write value to h.value
                                    if hasattr(self, 'write_value') and self.write_value is not None:
                                        h.value.CopyFrom(self.write_value)
                                
                                # Create broadcast message for internal write
                                msg_to_send = pb.Message()
                                msg_to_send.type = pb.Message.Type.BEB_BROADCAST
                                msg_to_send.FromAbstractionId = self.abstraction_id
                                msg_to_send.ToAbstractionId = f"{self.abstraction_id}.beb"
                                
                                # Create internal message
                                inner_message = pb.Message()
                                inner_message.type = pb.Message.Type.NNAR_INTERNAL_WRITE
                                inner_message.FromAbstractionId = self.abstraction_id
                                inner_message.ToAbstractionId = self.abstraction_id
                                
                                # Set fields for internal write
                                inner_message.nnarInternalWrite.readId = self.read_id
                                inner_message.nnarInternalWrite.timestamp = h.timestamp
                                inner_message.nnarInternalWrite.writerRank = h.writerRank
                                
                                # Copy value from h to internal write message
                                inner_message.nnarInternalWrite.value.CopyFrom(h.value)
                                
                                # Attach inner message to broadcast
                                msg_to_send.bebBroadcast.message.CopyFrom(inner_message)
                                # print("\ni hope it succeeded\n")
                    case pb.Message.Type.NNAR_INTERNAL_ACK:
                        # Get the internal acknowledgment message
                        v_msg = msg.plDeliver.message.nnarInternalAck

                        if v_msg.readId == self.read_id:
                            # Increment acknowledgment counter
                            self.acks = self.acks + 1
                            
                            # Check if we received a majority of acknowledgments
                            if self.acks > self.n // 2:
                                # Reset ack counter
                                self.acks = 0
                                
                                if self.reading:
                                    # If in reading mode, return the read value
                                    self.reading = False
                                    
                                    msg_to_send = pb.Message()
                                    msg_to_send.type = pb.Message.Type.NNAR_READ_RETURN
                                    msg_to_send.FromAbstractionId = self.abstraction_id
                                    msg_to_send.ToAbstractionId = "app"
                                    
                                    # Get the internal value and copy its Value field to the read return message
                                    internal_value = self._build_nnar_internal_value()
                                    msg_to_send.nnarReadReturn.value.CopyFrom(internal_value.value)
                                    
                                else:
                                    # If in writing mode, just send a write return message
                                    msg_to_send = pb.Message()
                                    msg_to_send.type = pb.Message.Type.NNAR_WRITE_RETURN
                                    msg_to_send.FromAbstractionId = self.abstraction_id
                                    msg_to_send.ToAbstractionId = "app"
                                    # NnarWriteReturn is empty, so no need to set fields
                                # print("\n\n\nhave i built a msg?\n\n\n")
                                # print(msg_to_send)
                                # print("\n\n")

        self.msg_queue.put(msg_to_send, block=False)

    def _build_nnar_internal_value(self):
        # default values won't appear in print
        nnar_internal_value = pb.NnarInternalValue()
        nnar_internal_value.readId = self.read_id
        nnar_internal_value.timestamp = self.timestamp

        value = pb.Value()
        value.defined = self.value != -1
        value.v = self.value

        nnar_internal_value.value.CopyFrom(value)

        return nnar_internal_value

    def _highest(self):
        highest = None
    
        for v in self.read_list.values():
            if highest is None:
                # Make a copy of the message to avoid modifying the one in read_list
                highest = pb.NnarInternalValue()
                highest.CopyFrom(v)
                continue
                
            # Compare current value with highest so far
            if self._compare(v, highest) == 1:
                highest.CopyFrom(v)
        
        return highest

    def _compare(self, v1, v2):
        if v1.timestamp > v2.timestamp:
            return 1
        if v2.timestamp > v1.timestamp:
            return -1
        
        # If timestamps are equal, compare writer ranks
        if v1.writerRank > v2.writerRank:
            return 1
        if v2.writerRank > v1.writerRank:
            return -1
        
        # Equal in both timestamp and writer rank
        return 0

    def _update_value(self, value):
        if value.defined:
            self.value = value.v
        else:
            self.value = -1
