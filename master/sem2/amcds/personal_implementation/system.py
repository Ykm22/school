import queue
import threading
from perfect_link import PerfectLink
from app import App
from best_effort_broadcast import BestEffortBroadcast
import pb.communication_protocol_pb2 as pb
import utils
from nnar import NNAtomicRegister
from consensus import EpochChange, EventualLeaderDetector, EventuallyPerfectFailureDetector, UniformConsensus

class System:
    def __init__(self, host_ip, host_port, owner, idx, hub_ip, hub_port, msg):
        print(f"Creating system {msg.systemId}")
        self.system_id = msg.systemId
        self.msg_queue = queue.Queue(maxsize=1024)
        self.hub_ip = hub_ip
        self.hub_port = hub_port
        self.processes = msg.procInitializeSystem.processes
        self.own_process = None
        self.abstractions = {}
        self.running = False
        self.event_thread = None
        
        for process in msg.procInitializeSystem.processes:
            if process.owner == owner and process.index == idx:
                self.own_process = process
                break
                
        self._register_abstractions()
        self._start_event_loop()
        
    def _register_abstractions(self):
        pl = PerfectLink(
            self.own_process.host, self.own_process.port, 
            self.hub_ip, self.hub_port, 
            self.system_id, self.msg_queue, self.processes
        )
        self.abstractions["app"] = App(self.msg_queue)
        self.abstractions["app.pl"] = pl.create_copy(parent_id="app")
        self.abstractions["app.beb"] = BestEffortBroadcast(self.msg_queue, self.processes, "app.beb")
        self.abstractions["app.beb.pl"] = pl.create_copy(parent_id="app.beb")

    def _register_nnar_abstractions(self, abstraction_id: str):
        pl = PerfectLink(
            self.own_process.host, self.own_process.port, 
            self.hub_ip, self.hub_port, 
            self.system_id, self.msg_queue, self.processes
        )
        self.abstractions[abstraction_id] = NNAtomicRegister(
            self.msg_queue, len(self.processes), 
            abstraction_id, 0, self.own_process.rank, 
            -1, {}
        )
        self.abstractions[f"{abstraction_id}.pl"] = pl.create_copy(parent_id=abstraction_id)
        self.abstractions[f"{abstraction_id}.beb"] = BestEffortBroadcast(self.msg_queue, self.processes, f"{abstraction_id}.beb")
        self.abstractions[f"{abstraction_id}.beb.pl"] = pl.create_copy(parent_id=f"{abstraction_id}.beb")
        # print(f"created register {abstraction_id}")

    def _register_consensus_abstractions(self, abstraction_id: str):
        # print("im here!\n\n\n")
        pl = PerfectLink(
            self.own_process.host, self.own_process.port, 
            self.hub_ip, self.hub_port, 
            self.system_id, self.msg_queue, self.processes
        )
        self.abstractions[abstraction_id] = UniformConsensus(abstraction_id, self.msg_queue, self.abstractions, self.processes, self.own_process, pl)
        self.abstractions[f"{abstraction_id}.ec"] = EpochChange(abstraction_id, f"{abstraction_id}.ec", self.msg_queue, self.processes, self.own_process)
        self.abstractions[f"{abstraction_id}.ec.pl"] = pl.create_copy(parent_id=f"{abstraction_id}.ec")
        self.abstractions[f"{abstraction_id}.ec.beb"] = BestEffortBroadcast(self.msg_queue, self.processes, f"{abstraction_id}.ec.beb")
        self.abstractions[f"{abstraction_id}.ec.beb.pl"] = pl.create_copy(parent_id=f"{abstraction_id}.ec.beb")
        self.abstractions[f"{abstraction_id}.ec.eld"] = EventualLeaderDetector(f"{abstraction_id}.ec", f"{abstraction_id}.ec.eld", self.msg_queue, self.processes)
        self.abstractions[f"{abstraction_id}.ec.eld.epfd"] = EventuallyPerfectFailureDetector(f"{abstraction_id}.ec.eld", f"{abstraction_id}.ec.eld.epfd", self.msg_queue, self.processes)
        # print("aloo\n\n\n")
        self.abstractions[f"{abstraction_id}.ec.eld.epfd.pl"] = pl.create_copy(parent_id=f"{abstraction_id}.ec.eld.epfd")
        # print("aloo\n\n\n")
        
    def _start_event_loop(self):
        self.running = True
        self.event_thread = threading.Thread(target=self._event_loop, daemon=True)
        self.event_thread.start()
        print(f"Event loop started for system {self.system_id}")
        
    def _event_loop(self):
        while self.running:
            try:
                message = self.msg_queue.get(block=True, timeout=0.1)
                self._process_message(message)
                self.msg_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in event loop for system {self.system_id}: {str(e)}")
                
    def _process_message(self, msg: pb.Message):
        # print("have to process message!")
        # print(msg)
        to_abstraction_id = msg.ToAbstractionId
        if to_abstraction_id not in self.abstractions.keys():
            # print("\n\n")
            # print(to_abstraction_id)
            # print("\n\n")
            # print(msg.type)
            # print("\n\n")
            if to_abstraction_id.startswith("app.nnar"):
                register_id = utils.extract_register_id(to_abstraction_id)
                if register_id:
                    self._register_nnar_abstractions(f"app.nnar[{register_id}]")
                else:
                    print(f"Error extracting NNAR register_id: {register_id}")
            elif msg.type == pb.Message.Type.UC_PROPOSE:
                register_id = utils.extract_register_id(to_abstraction_id)
                if register_id:
                    self._register_consensus_abstractions(f"app.uc[{register_id}]")
                else:
                    print(f"Error extracting UC_PROPOSE register_id: {register_id}")
        try:
            # print(self.abstractions.keys())
            handler = self.abstractions[msg.ToAbstractionId]
            handler.handle(msg)
        except Exception as e:
            print(f"No handler: {str(e)}")
            
    def add_message(self, msg: pb.Message):
        try:
            self.msg_queue.put(msg, block=False)
            return True
        except queue.Full:
            print(f"Message queue full for system {self.system_id}")
            return False
        except Exception as e:
            print(f"Error adding message to queue: {str(e)}")
            return False
            
    def destroy(self):
        print("have to destroy system!")
        pass
