import pb.communication_protocol_pb2 as pb
from tcp import tcp 
import queue

#         pl = PerfectLink(self.own_process.host, self.own_process.port, self.hub_ip, self.hub_port, self.system_id, self.msg_queue, self.processes)


class PerfectLink():
    def __init__(self, host, port, hub_ip, hub_port, system_id="0", msg_queue=queue.Queue(), processes=None, parent_id=None):
        self.host = host
        self.port = port
        self.hub_ip = hub_ip
        self.hub_port = hub_port

        self.system_id = system_id
        self.msg_queue = msg_queue
        self.processes = processes

        self.parent_id = parent_id

    def _send(self, msg: pb.Message) -> bool:
        try:
            _msg = pb.Message()
            _msg.systemId = self.system_id
            _msg.ToAbstractionId = msg.ToAbstractionId
            _msg.type = pb.Message.Type.NETWORK_MESSAGE
            
            # Initialize the networkMessage field
            _msg.networkMessage.senderHost = self.host
            _msg.networkMessage.senderListeningPort = self.port
            _msg.networkMessage.message.CopyFrom(msg.plSend.message)
            
            serialized_msg = _msg.SerializeToString() 

            ip_dest = self.hub_ip
            port_dest = self.hub_port
            # is_true = False

            if msg.plSend.HasField("destination"):
                # print(msg.plSend.destination)
                # print(msg)
                # is_true = True
                ip_dest = msg.plSend.destination.host
                port_dest = str(msg.plSend.destination.port)

            # print(f"ip_dest = {ip_dest}, port_dest = {port_dest}, is_true = {is_true}")
            success = tcp.send(ip_dest, port_dest, serialized_msg)
            return success
        except Exception as e:
            print(f"Error in _send: {str(e)}")
            return False
        

    def handle(self, msg: pb.Message) -> bool:
        print(f"Handling message of type: {msg.type}")
        try:
            match msg.type:
                case pb.Message.Type.PL_SEND:
                    return self._send(msg)
                case pb.Message.Type.NETWORK_MESSAGE:
                    sender = None
                    for process in self.processes:
                        if process.host == msg.networkMessage.senderHost and process.port == msg.networkMessage.senderListeningPort:
                            sender = process
                            break

                    _msg = pb.Message()
                    _msg.systemId = msg.systemId
                    _msg.FromAbstractionId = msg.FromAbstractionId
                    _msg.ToAbstractionId = self.parent_id
                    _msg.type = pb.Message.Type.PL_DELIVER

                    # print(sender)
                    # if from hub, sender isn't in my processes list
                    if sender is None:
                        _msg.plDeliver.sender.Clear()
                    else:
                        _msg.plDeliver.sender.CopyFrom(sender)

                    # print(msg.networkMessage.message)
                    _msg.plDeliver.message.CopyFrom(msg.networkMessage.message)

                    self.msg_queue.put(_msg, block=False)
                case _:
                    print(f"No handler for message type: {msg.type}")
                    return False
        except Exception as e:
            print(f"Error handling message: {str(e)}")
            return False

    def create_copy(self, **kwargs):
        params = {
            "host": self.host,
            "port": self.port,
            "hub_ip": self.hub_ip,
            "hub_port": self.hub_port,
            "system_id": self.system_id,
            "msg_queue": self.msg_queue,
            "processes": self.processes,
            "parent_id": self.parent_id,
        }
        
        params.update(kwargs)
        new_instance = PerfectLink(**params)
        
        return new_instance
