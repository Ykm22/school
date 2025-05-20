import queue
import pb.communication_protocol_pb2 as pb


class EpochConsensus():
    def __init__(self, parent_abstraction_id: str, abstraction_id: str, msg_queue: queue.Queue, processes: list, epoch_timestamp, value, value_timestamp):
        self.parent_abstraction_id = parent_abstraction_id
        self.abstraction_id = abstraction_id
        self.msg_queue = msg_queue
        self.processes = processes
        
        self.aborted = False
        self.epoch_timestamp = epoch_timestamp
        self.temp_value = pb.Value()
        self.accepted = 0

        self.value = value
        self.value_timestamp = value_timestamp
        self.states = {}

    def handle(self, msg: pb.Message):
        if self.aborted:
            return None
        
        if msg.type == pb.Message.Type.EP_PROPOSE:
            self.temp_value.CopyFrom(msg.epPropose.value)
            # Create a message for BEB_BROADCAST
            broadcast_msg = pb.Message()
            broadcast_msg.type = pb.Message.Type.BEB_BROADCAST
            broadcast_msg.FromAbstractionId = self.abstraction_id
            broadcast_msg.ToAbstractionId = f"{self.abstraction_id}.beb"

            # Create the inner message for EP_INTERNAL_READ
            inner_message = pb.Message()
            inner_message.type = pb.Message.Type.EP_INTERNAL_READ
            inner_message.FromAbstractionId = self.abstraction_id
            inner_message.ToAbstractionId = self.abstraction_id
            # EpInternalRead is empty, so no fields to set

            # Attach inner message to broadcast
            broadcast_msg.bebBroadcast.message.CopyFrom(inner_message)

            # Add message to the queue
            self.msg_queue.put(broadcast_msg)

        elif msg.type == pb.Message.Type.EP_ABORT:
            # Create a message for EP_ABORTED
            aborted_msg = pb.Message()
            aborted_msg.type = pb.Message.Type.EP_ABORTED
            aborted_msg.FromAbstractionId = self.abstraction_id
            aborted_msg.ToAbstractionId = self.parent_abstraction_id

            # Set the fields in the EpAborted message
            aborted_msg.epAborted.ets = self.epoch_timestamp
            aborted_msg.epAborted.valueTimestamp = self.value_timestamp
            aborted_msg.epAborted.value.CopyFrom(self.value)

            # Add message to the queue
            self.msg_queue.put(aborted_msg)

            # Set aborted flag to True
            self.aborted = True

        elif msg.type == pb.Message.Type.PL_DELIVER:
            internal_message = msg.plDeliver.message
            if internal_message.type == pb.Message.Type.EP_INTERNAL_STATE:
                # Store the state from the sender
                sender = msg.plDeliver.sender
                sender_key = f"{sender.owner}-{sender.index}"
                self.states[sender_key] = {
                    'value_timestamp': msg.plDeliver.message.epInternalState.valueTimestamp,
                    # this works?
                    'value': msg.plDeliver.message.epInternalState.value.CopyFrom()  # Create a copy
                }

                # Check if we have received states from a majority of processes
                if len(self.states) > len(self.processes) // 2:  # Integer division in Python
                    # Get highest state
                    highest_state = self._highest()
                    
                    # If highest state has a defined value, use it
                    if (highest_state is not None and 
                            highest_state['value'] is not None and 
                            highest_state['value'].defined):
                        self.temp_value.CopyFrom(highest_state['value'])
                    
                    # Reset states collection
                    self.states = {}
                    
                    # Create a message for BEB_BROADCAST
                    broadcast_msg = pb.Message()
                    broadcast_msg.type = pb.Message.Type.BEB_BROADCAST
                    broadcast_msg.FromAbstractionId = self.abstraction_id
                    broadcast_msg.ToAbstractionId = f"{self.abstraction_id}.beb"
                    
                    # Create the inner message for EP_INTERNAL_WRITE
                    inner_message = pb.Message()
                    inner_message.type = pb.Message.Type.EP_INTERNAL_WRITE
                    inner_message.FromAbstractionId = self.abstraction_id
                    inner_message.ToAbstractionId = self.abstraction_id
                    
                    # Set the value in the write message
                    inner_message.epInternalWrite.value.CopyFrom(self.temp_value)
                    
                    # Attach inner message to broadcast
                    broadcast_msg.bebBroadcast.message.CopyFrom(inner_message)
                    
                    # Add message to the queue
                    self.msg_queue.put(broadcast_msg)

            elif internal_message.type == pb.Message.Type.EP_INTERNAL_ACCEPT:
                # Increment the accepted counter
                self.accepted += 1

                # Check if we have received acceptances from a majority of processes
                if self.accepted > len(self.processes) // 2:  # Integer division in Python
                    # Reset accepted counter
                    self.accepted = 0
                    
                    # Create a message for BEB_BROADCAST
                    broadcast_msg = pb.Message()
                    broadcast_msg.type = pb.Message.Type.BEB_BROADCAST
                    broadcast_msg.FromAbstractionId = self.abstraction_id
                    broadcast_msg.ToAbstractionId = f"{self.abstraction_id}.beb"
                    
                    # Create the inner message for EP_INTERNAL_DECIDED
                    inner_message = pb.Message()
                    inner_message.type = pb.Message.Type.EP_INTERNAL_DECIDED
                    inner_message.FromAbstractionId = self.abstraction_id
                    inner_message.ToAbstractionId = self.abstraction_id
                    
                    # Set the value in the decided message
                    inner_message.epInternalDecided.value.CopyFrom(self.temp_value)
                    
                    # Attach inner message to broadcast
                    broadcast_msg.bebBroadcast.message.CopyFrom(inner_message)
                    
                    # Add message to the queue
                    self.msg_queue.put(broadcast_msg)

            pass

        elif msg.type == pb.Message.Type.BEB_DELIVER:
            internal_message = msg.bebDeliver.message

            if internal_message.type == pb.Message.Type.EP_INTERNAL_READ:
                # Create a message for PL_SEND
                state_msg = pb.Message()
                state_msg.type = pb.Message.Type.PL_SEND
                state_msg.FromAbstractionId = self.abstraction_id
                state_msg.ToAbstractionId = f"{self.abstraction_id}.pl"

                # Create the inner message for EP_INTERNAL_STATE
                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.EP_INTERNAL_STATE
                inner_message.FromAbstractionId = self.abstraction_id
                inner_message.ToAbstractionId = self.abstraction_id

                # Set the state fields
                inner_message.epInternalState.valueTimestamp = self.value_timestamp
                inner_message.epInternalState.value.CopyFrom(self.value)

                # Set destination and inner message in PlSend
                state_msg.plSend.destination.CopyFrom(msg.bebDeliver.sender)
                state_msg.plSend.message.CopyFrom(inner_message)

                # Add message to the queue
                self.msg_queue.put(state_msg)


            elif internal_message.type == pb.Message.Type.EP_INTERNAL_WRITE:
                # Update the state with the received value
                self.value_timestamp = self.epoch_timestamp
                self.value.CopyFrom(msg.bebDeliver.message.epInternalWrite.value)

                # Create a message for PL_SEND
                accept_msg = pb.Message()
                accept_msg.type = pb.Message.Type.PL_SEND
                accept_msg.FromAbstractionId = self.abstraction_id
                accept_msg.ToAbstractionId = f"{self.abstraction_id}.pl"

                # Create the inner message for EP_INTERNAL_ACCEPT
                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.EP_INTERNAL_ACCEPT
                inner_message.FromAbstractionId = self.abstraction_id
                inner_message.ToAbstractionId = self.abstraction_id
                # EpInternalAccept is empty, so no fields to set

                # Set destination and inner message in PlSend
                accept_msg.plSend.destination.CopyFrom(msg.bebDeliver.sender)
                accept_msg.plSend.message.CopyFrom(inner_message)
                
                # Add message to the queue
                self.msg_queue.put(accept_msg)

            elif internal_message.type == pb.Message.Type.EP_INTERNAL_DECIDED:
                # Create a message for EP_DECIDE
                decide_msg = pb.Message()
                decide_msg.type = pb.Message.Type.EP_DECIDE
                decide_msg.FromAbstractionId = self.abstraction_id
                decide_msg.ToAbstractionId = self.parent_abstraction_id

                # Set the fields in the EpDecide message
                decide_msg.epDecide.ets = self.epoch_timestamp
                decide_msg.epDecide.value.CopyFrom(self.value)

                # Add message to the queue
                self.msg_queue.put(decide_msg)
            pass


    def _highest(self):
        highest_state = {'value_timestamp': 0, 'value': None}
    
        # Iterate through all states
        for state in self.states.values():
            if state['value_timestamp'] > highest_state['value_timestamp']:
                highest_state = state
        
        return highest_state
