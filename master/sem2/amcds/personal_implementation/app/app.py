import queue
import pb.communication_protocol_pb2 as pb

class App():
    def __init__(self, msg_queue: queue.Queue):
        self.msg_queue = msg_queue

    def handle(self, msg: pb.Message):
        msg_to_send = None
        # print(msg)
        match msg.type:
            case pb.Message.Type.PL_DELIVER:
                match msg.plDeliver.message.type:
                    case pb.Message.Type.APP_BROADCAST:
                        # print("broadcast from app to beb")
                        msg_to_send = pb.Message()
                        msg_to_send.type = pb.Message.Type.BEB_BROADCAST
                        msg_to_send.FromAbstractionId = "app"
                        msg_to_send.ToAbstractionId = "app.beb"
                        # Create the inner message for BEB broadcast
                        inner_message = pb.Message()
                        inner_message.type = pb.Message.Type.APP_VALUE
                        inner_message.FromAbstractionId = "app"
                        inner_message.ToAbstractionId = "app"

                        inner_message.appValue.value.CopyFrom(msg.plDeliver.message.appBroadcast.value)

                        msg_to_send.bebBroadcast.message.CopyFrom(inner_message)

                    case pb.Message.Type.APP_VALUE:
                        # print("value from app to pl")
                        msg_to_send = pb.Message()
                        msg_to_send.type = pb.Message.Type.PL_SEND
                        msg_to_send.FromAbstractionId = "app"
                        msg_to_send.ToAbstractionId = "app.pl"

                        inner_message = pb.Message()
                        inner_message.type = pb.Message.Type.APP_VALUE
                        inner_message.appValue.CopyFrom(msg.plDeliver.message.appValue)

                        msg_to_send.plSend.message.CopyFrom(inner_message)

            case pb.Message.Type.BEB_DELIVER:
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.Type.PL_SEND
                msg_to_send.FromAbstractionId = "app"
                msg_to_send.ToAbstractionId = "app.pl"

                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.APP_VALUE
                inner_message.appValue.CopyFrom(msg.bebDeliver.message.appValue)

                msg_to_send.plSend.message.CopyFrom(inner_message)
        self.msg_queue.put(msg_to_send, block=False)
