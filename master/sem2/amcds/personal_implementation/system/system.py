import queue
import threading
import time
from pl.perfect_link import PerfectLink
from app.app import App
from broadcast.best_effort_broadcast import BestEffortBroadcast
import pb.communication_protocol_pb2 as pb

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
        
    def _start_event_loop(self):
        self.running = True
        self.event_thread = threading.Thread(target=self._event_loop, daemon=True)
        self.event_thread.start()
        print(f"Event loop started for system {self.system_id}")
        
    def _event_loop(self):
        while self.running:
            try:
                # Non-blocking queue get with timeout to allow checking running flag
                message = self.msg_queue.get(block=True, timeout=0.1)
                self._process_message(message)
                self.msg_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in event loop for system {self.system_id}: {str(e)}")
                
    def _process_message(self, msg: pb.Message):
        # print("have to process message!")
        handler = self.abstractions[msg.ToAbstractionId]
        handler.handle(msg)
        pass
            
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
