import queue
import pb.communication_protocol_pb2 as pb

class BestEffortBroadcast():
    def __init__(self, msg_queue: queue.Queue, processes: list, id: str):
        self.msg_queue = msg_queue
        self.processes = processes
        self.id = id

    def handle(self, msg: pb.Message):
        # print(msg)
        _msg = None

        match msg.type:
            case pb.Message.Type.BEB_BROADCAST:
                for process in self.processes:
                    _msg = pb.Message()
                    _msg.type = pb.Message.Type.PL_SEND
                    _msg.FromAbstractionId = self.id
                    _msg.ToAbstractionId = f"{self.id}.pl"
                    
                    inner_message = msg.bebBroadcast.message

                    # print("process =")
                    # print(process)
                    # print("\n\n")
                    _msg.plSend.destination.CopyFrom(process)
                    _msg.plSend.message.CopyFrom(inner_message)
                    # print(_msg)
                    self.msg_queue.put(_msg, block=False)
            case pb.Message.Type.PL_DELIVER:
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.Type.BEB_DELIVER
                msg_to_send.FromAbstractionId = self.id
                msg_to_send.ToAbstractionId = msg.plDeliver.message.ToAbstractionId

                msg_to_send.bebDeliver.sender.CopyFrom(msg.plDeliver.sender)
                msg_to_send.bebDeliver.message.CopyFrom(msg.plDeliver.message)

                self.msg_queue.put(msg_to_send)
