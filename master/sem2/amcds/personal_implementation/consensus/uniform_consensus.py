import queue
import utils
from best_effort_broadcast import BestEffortBroadcast
import pb.communication_protocol_pb2 as pb
from consensus.epoch_consensus import EpochConsensus

class UniformConsensus():
    def __init__(self, abstraction_id: str, msg_queue: queue.Queue, abstractions: dict, processes: list, own_process, pl):
        self.abstraction_id = abstraction_id
        self.msg_queue = msg_queue
        self.abstractions = abstractions
        self.processes = processes
        self.own_process = own_process
        self.pl = pl

        self.value = pb.Value()

        self.proposed = False
        self.decided = False

        self.epoch_timestamp = 0

        self.leader = utils.get_max_rank_slice(self.processes)
        self.new_timestamp = 0
        self.new_leader = pb.ProcessId()

        self._add_epoch_consensus_abstraction()

    def _get_epoch_consensus_id(self):
        return f".ep[{str(self.epoch_timestamp)}]"

    def _add_epoch_consensus_abstraction(self, value=pb.Value(), value_timestamp=0):
        abstraction_id = self.abstraction_id + self._get_epoch_consensus_id()

        self.abstractions[abstraction_id] = EpochConsensus(self.abstraction_id, abstraction_id, self.msg_queue, self.processes, self.epoch_timestamp, value, value_timestamp)
        self.abstractions[f"{abstraction_id}.pl"] = self.pl.create_copy(parent_id=abstraction_id)

        self.abstractions[f"{abstraction_id}.beb"] = BestEffortBroadcast(self.msg_queue, self.processes, f"{abstraction_id}.beb")
        self.abstractions[f"{abstraction_id}.beb.pl"] = self.pl.create_copy(parent_id=f"{abstraction_id}.beb")

    def handle(self, msg: pb.Message):
        if msg.type == pb.Message.Type.UC_PROPOSE:
            self.value.CopyFrom(msg.ucPropose.value)

        elif msg.type == pb.Message.Type.EC_START_EPOCH:
            self.new_timestamp = msg.ecStartEpoch.newTimestamp
            self.new_leader = msg.ecStartEpoch.newLeader

            abort_msg = pb.Message()
            abort_msg.type = pb.Message.Type.EP_ABORT
            abort_msg.FromAbstractionId = self.abstraction_id
            abort_msg.ToAbstractionId = f"{self.abstraction_id}{self._get_epoch_consensus_id()}"

            self.msg_queue.put(abort_msg)

        elif msg.type == pb.Message.Type.EP_ABORTED:
            if self.epoch_timestamp == msg.epAborted.ets:
                self.epoch_timestamp = self.new_timestamp
                self.leader = self.new_leader
                self.proposed = False
                
                # might not work without CopyFrom()
                self._add_epoch_consensus_abstraction(value=msg.epAborted.value, value_timestamp=self.epoch_timestamp)

        elif msg.type == pb.Message.Type.EP_DECIDE:
            if self.epoch_timestamp == msg.epDecide.ets and not self.decided:
                self.decided = True

                decide_msg = pb.Message()
                decide_msg.type = pb.Message.Type.UC_DECIDE
                decide_msg.FromAbstractionId = self.abstraction_id
                decide_msg.ToAbstractionId = "app"

                # Copy the value from the EpDecide message
                decide_msg.ucDecide.value.CopyFrom(msg.epDecide.value)

                # Add message to the queue
                self.msg_queue.put(decide_msg)

        self._update_leader()

    def _update_leader(self):
        leader_key = f"{self.leader.owner}-{self.leader.index}"
        abstraction_key = f"{self.own_process.owner}-{self.own_process.index}"

        if leader_key == abstraction_key and self.value.defined and not self.proposed:
            self.proposed = True

            # Create a message for EP_PROPOSE
            propose_msg = pb.Message()
            propose_msg.type = pb.Message.Type.EP_PROPOSE
            propose_msg.FromAbstractionId = self.abstraction_id
            propose_msg.ToAbstractionId = f"{self.abstraction_id}{self._get_epoch_consensus_id()}"
            
            # Copy the value to the proposal
            propose_msg.epPropose.value.CopyFrom(self.value)
            
            # Add message to the queue
            self.msg_queue.put(propose_msg)
