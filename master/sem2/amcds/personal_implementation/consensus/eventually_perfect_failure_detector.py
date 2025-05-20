import queue
import threading
import pb.communication_protocol_pb2 as pb

DELTA = 0.1

class EventuallyPerfectFailureDetector():
    def __init__(self, parent_abstraction_id: str, abstraction_id: str, msg_queue: queue.Queue, processes: list):
        self.parent_abstraction_id = parent_abstraction_id
        self.abstraction_id = abstraction_id
        self.msg_queue = msg_queue
        self.processes = processes

        self.alive = {}
        self.suspected = {}
        self.delay = DELTA

        for process in self.processes:
            self.alive[f"{process.owner}-{process.index}"] = process

        self.timer = None
        self._start_timer()

    def _start_timer(self):
        self._stop_timer()
        self.timer = threading.Timer(self.delay, self._timer_callback)
        self.timer.daemon = True
        self.timer.start()

    def _stop_timer(self):
        if self.timer is not None and self.timer.is_alive():
            self.timer.cancel()
            self.timer = None

    def _timer_callback(self):
        msg_to_send = pb.Message()
        msg_to_send.type = pb.Message.Type.EPFD_TIMEOUT
        msg_to_send.FromAbstractionId = self.abstraction_id
        msg_to_send.ToAbstractionId = self.abstraction_id
        # EpfdTimeout is empty, so no need to set fields
        
        self.msg_queue.put(msg_to_send)

    def handle(self, msg: pb.Message):
        try:
            if msg.type == pb.Message.Type.EPFD_TIMEOUT:
                self._handle_timeout()
            elif msg.type == pb.Message.Type.PL_DELIVER:
                inner_msg_type = msg.plDeliver.message.type
                if inner_msg_type == pb.Message.Type.EPFD_INTERNAL_HEARTBEAT_REQUEST:
                    # Create heartbeat reply message
                    reply_msg = pb.Message()
                    reply_msg.type = pb.Message.Type.PL_SEND
                    reply_msg.FromAbstractionId = self.abstraction_id
                    reply_msg.ToAbstractionId = f"{self.abstraction_id}.pl"
                    
                    # Create inner message for heartbeat reply
                    inner_message = pb.Message()
                    inner_message.type = pb.Message.Type.EPFD_INTERNAL_HEARTBEAT_REPLY
                    inner_message.FromAbstractionId = self.abstraction_id
                    inner_message.ToAbstractionId = self.abstraction_id
                    # No fields to set for EpfdInternalHeartbeatReply
                    
                    # Set inner message in PlSend
                    reply_msg.plSend.message.CopyFrom(inner_message)
                    
                    # Destination should be the sender of the request
                    reply_msg.plSend.destination.CopyFrom(msg.plDeliver.sender)
                    
                    # Put message in the queue
                    self.msg_queue.put(reply_msg)
                    return True
                elif inner_msg_type == pb.Message.Type.EPFD_INTERNAL_HEARTBEAT_REPLY:
                    # Mark process as alive
                    sender = msg.plDeliver.sender
                    process_key = f"{sender.owner}-{sender.index}"
                    self.alive[process_key] = msg.plDeliver.sender
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"Error in epfd.handle: {str(e)}")
            return False

    def _handle_timeout(self):
        for k in self.suspected:
            if k in self.alive:
                self.delay = self.delay + DELTA
                print(f"Increased timeout to {self.delay}")
                break
        
        # Check all processes for suspect/restore status
        for process in self.processes:
            key = f"{process.owner}-{process.index}"
            is_alive = key in self.alive
            is_suspected = key in self.suspected
            
            if not is_alive and not is_suspected:
                # Process is newly suspected
                self.suspected[key] = process
                
                # Create and send EPFD_SUSPECT message
                suspect_msg = pb.Message()
                suspect_msg.type = pb.Message.Type.EPFD_SUSPECT
                suspect_msg.FromAbstractionId = self.abstraction_id
                suspect_msg.ToAbstractionId = self.parent_abstraction_id
                suspect_msg.epfdSuspect.process.CopyFrom(process)
                
                # Queue the message
                self.msg_queue.put(suspect_msg)
                
            elif is_alive and is_suspected:
                # Process is restored
                del self.suspected[key]
                
                # Create and send EPFD_RESTORE message
                restore_msg = pb.Message()
                restore_msg.type = pb.Message.Type.EPFD_RESTORE
                restore_msg.FromAbstractionId = self.abstraction_id
                restore_msg.ToAbstractionId = self.parent_abstraction_id
                restore_msg.epfdRestore.process.CopyFrom(process)
                
                # Queue the message
                self.msg_queue.put(restore_msg)
            
            # Send heartbeat request to each process
            heartbeat_msg = pb.Message()
            heartbeat_msg.type = pb.Message.Type.PL_SEND
            heartbeat_msg.FromAbstractionId = self.abstraction_id
            heartbeat_msg.ToAbstractionId = f"{self.abstraction_id}.pl"
            
            # Create inner heartbeat request message
            inner_msg = pb.Message()
            inner_msg.type = pb.Message.Type.EPFD_INTERNAL_HEARTBEAT_REQUEST
            inner_msg.FromAbstractionId = self.abstraction_id
            inner_msg.ToAbstractionId = self.abstraction_id
            # No fields to set for EpfdInternalHeartbeatRequest
            
            # Set destination and inner message
            heartbeat_msg.plSend.destination.CopyFrom(process)
            heartbeat_msg.plSend.message.CopyFrom(inner_msg)
            
            # Queue the message
            self.msg_queue.put(heartbeat_msg)
        
        # Reset the alive map and restart the timer
        self.alive = {}
        self._start_timer()
