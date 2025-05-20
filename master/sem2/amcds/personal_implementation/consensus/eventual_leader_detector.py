import queue
import utils
import pb.communication_protocol_pb2 as pb

class EventualLeaderDetector():
    def __init__(self, parent_abstraction_id: str, abstraction_id: str, msg_queue: queue.Queue, processes: list):
        self.parent_abstraction_id = parent_abstraction_id
        self.abstraction_id = abstraction_id
        self.msg_queue = msg_queue
        self.processes = processes

        self.alive = {}
        self.leader = None

        for process in processes:
            self.alive[f"{process.owner}-{process.index}"] = process

    def handle(self, msg: pb.Message):
        if msg.type == pb.Message.Type.EPFD_SUSPECT:
            process = msg.epfdSuspect.process
            key = f"{process.owner}-{process.index}"
            self.alive.pop(key, None)
        
        elif msg.type == pb.Message.Type.EPFD_RESTORE:
            process = msg.epfdSuspect.process
            key = f"{process.owner}-{process.index}"
            self.alive[key] = process

        self._update_leader()

    def _update_leader(self):
        max_rank_proc = utils.get_max_rank(self.alive)

        if max_rank_proc is None:
            print("Error in finding process with max rank")
            return

        leader_key = f"{self.leader.owner}-{self.leader.index}" if self.leader else None
        max_proc_key = f"{max_rank_proc.owner}-{max_rank_proc.index}"


        if self.leader is None or leader_key != max_proc_key:
            # Update the leader
            self.leader = max_rank_proc
            
            # Create and send the ELD_TRUST message
            trust_msg = pb.Message()
            trust_msg.type = pb.Message.Type.ELD_TRUST
            trust_msg.FromAbstractionId = self.abstraction_id
            trust_msg.ToAbstractionId = self.parent_abstraction_id
            
            # Set the process field in EldTrust
            trust_msg.eldTrust.process.CopyFrom(self.leader)
            
            # Put the message in the queue
            self.msg_queue.put(trust_msg)
