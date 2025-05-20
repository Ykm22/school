import queue
import utils
import pb.communication_protocol_pb2 as pb

class EpochChange():
    def __init__(self, parent_abstraction_id: str, abstraction_id: str, msg_queue: queue.Queue, processes: list, own_process):
        self.parent_abstraction_id = parent_abstraction_id
        self.abstraction_id = abstraction_id
        self.msg_queue = msg_queue
        self.processes = processes
        self.own_process = own_process

        self.trusted = utils.get_max_rank_slice(processes)
        self.last_timestamp = 0
        self.timestamp = self.own_process.rank

    def handle(self, msg: pb.Message):
        if msg.type == pb.Message.Type.ELD_TRUST:
            self.trusted = msg.eldTrust.process

            own_process_key = f"{self.own_process.owner}-{self.own_process.index}"
            trusted_key = f"{self.trusted.owner}-{self.trusted.index}"
            if own_process_key == trusted_key:
                self.timestamp = self.timestamp + len(self.processes)
                # Create broadcast message
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.Type.BEB_BROADCAST
                msg_to_send.FromAbstractionId = self.abstraction_id
                msg_to_send.ToAbstractionId = f"{self.abstraction_id}.beb"
                
                # Create inner message for new epoch
                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.EC_INTERNAL_NEW_EPOCH
                inner_message.FromAbstractionId = self.abstraction_id
                inner_message.ToAbstractionId = self.abstraction_id
                
                # Set timestamp in the new epoch message
                inner_message.ecInternalNewEpoch.timestamp = self.timestamp
                
                # Attach inner message to broadcast
                msg_to_send.bebBroadcast.message.CopyFrom(inner_message)
                
                # Queue the message
                self.msg_queue.put(msg_to_send)

        elif msg.type == pb.Message.Type.PL_DELIVER:
            if msg.plDeliver.message.type == pb.Message.Type.EC_INTERNAL_NACK:
                own_process_key = f"{self.own_process.owner}-{self.own_process.index}"
                trusted_key = f"{self.trusted.owner}-{self.trusted.index}"
                if own_process_key == trusted_key:
                    self.timestamp = self.timestamp + len(self.processes)
                    # Create broadcast message
                    msg_to_send = pb.Message()
                    msg_to_send.type = pb.Message.Type.BEB_BROADCAST
                    msg_to_send.FromAbstractionId = self.abstraction_id
                    msg_to_send.ToAbstractionId = f"{self.abstraction_id}.beb"
                    
                    # Create inner message for new epoch
                    inner_message = pb.Message()
                    inner_message.type = pb.Message.Type.EC_INTERNAL_NEW_EPOCH
                    inner_message.FromAbstractionId = self.abstraction_id
                    inner_message.ToAbstractionId = self.abstraction_id
                    
                    # Set timestamp in the new epoch message
                    inner_message.ecInternalNewEpoch.timestamp = self.timestamp
                    
                    # Attach inner message to broadcast
                    msg_to_send.bebBroadcast.message.CopyFrom(inner_message)
                    
                    # Queue the message
                    self.msg_queue.put(msg_to_send)


        elif msg.type == pb.Message.Type.BEB_DELIVER:
            internal_message = msg.bebDeliver.message
            if internal_message.type == pb.Message.Type.EC_INTERNAL_NEW_EPOCH:
                new_timestamp = internal_message.ecInternalNewEpoch.timestamp

                sender = msg.bebDeliver.sender
                sender_key = f"{sender.owner}-{sender.index}"
                trusted_key = f"{self.trusted.owner}-{self.trusted.index}"

                if sender_key == trusted_key and new_timestamp > self.last_timestamp:
                    self.last_timestamp = new_timestamp
                    start_epoch_msg = pb.Message()
                    start_epoch_msg.type = pb.Message.Type.EC_START_EPOCH
                    start_epoch_msg.FromAbstractionId = self.abstraction_id
                    start_epoch_msg.ToAbstractionId = self.parent_abstraction_id

                    # Set the fields in the EcStartEpoch message
                    start_epoch_msg.ecStartEpoch.newTimestamp = new_timestamp
                    start_epoch_msg.ecStartEpoch.newLeader.CopyFrom(msg.bebDeliver.sender)

                    # Then add the message to the queue
                    self.msg_queue.put(start_epoch_msg)

                else:
                    # First, create the outer message for PL_SEND
                    pl_send_msg = pb.Message()
                    pl_send_msg.type = pb.Message.Type.PL_SEND
                    pl_send_msg.FromAbstractionId = self.abstraction_id
                    pl_send_msg.ToAbstractionId = f"{self.abstraction_id}.pl"

                    # Create the inner message for EC_INTERNAL_NACK
                    inner_message = pb.Message()
                    inner_message.type = pb.Message.Type.EC_INTERNAL_NACK
                    inner_message.FromAbstractionId = self.abstraction_id
                    inner_message.ToAbstractionId = self.abstraction_id
                    # EcInternalNack is empty, so no fields to set

                    # Set destination and inner message in PlSend
                    pl_send_msg.plSend.destination.CopyFrom(msg.bebDeliver.sender)
                    pl_send_msg.plSend.message.CopyFrom(inner_message)

                    # Then add the message to the queue
                    self.msg_queue.put(pl_send_msg)
