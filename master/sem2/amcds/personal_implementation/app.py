import queue
import pb.communication_protocol_pb2 as pb
import utils

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

                    case pb.Message.Type.APP_WRITE:
                        # Create message for NNAR_WRITE
                        msg_to_send = pb.Message()
                        msg_to_send.type = pb.Message.Type.NNAR_WRITE
                        msg_to_send.FromAbstractionId = "app"

                        register = msg.plDeliver.message.appWrite.register
                        msg_to_send.ToAbstractionId = f"app.nnar[{register}]"

                        msg_to_send.nnarWrite.value.CopyFrom(msg.plDeliver.message.appWrite.value)
                    case pb.Message.Type.APP_READ:
                        msg_to_send = pb.Message()
                        msg_to_send.type = pb.Message.Type.NNAR_READ
                        msg_to_send.FromAbstractionId = "app"
                        msg_to_send.ToAbstractionId = f"app.nnar[{msg.plDeliver.message.appRead.register}]"
                        msg_to_send.nnarRead.SetInParent()  # Equivalent to creating an empty NnarRead message
                    case pb.Message.Type.APP_PROPOSE:
                        # Create message for UC_PROPOSE
                        msg_to_send = pb.Message()
                        msg_to_send.type = pb.Message.Type.UC_PROPOSE
                        msg_to_send.FromAbstractionId = "app"

                        # Build the ToAbstractionId with the topic name
                        topic = msg.plDeliver.message.appPropose.topic
                        msg_to_send.ToAbstractionId = f"app.uc[{topic}]"

                        # Copy the value from the original message to UcPropose
                        msg_to_send.ucPropose.value.CopyFrom(msg.plDeliver.message.appPropose.value)

            case pb.Message.Type.BEB_DELIVER:
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.Type.PL_SEND
                msg_to_send.FromAbstractionId = "app"
                msg_to_send.ToAbstractionId = "app.pl"

                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.APP_VALUE
                inner_message.appValue.CopyFrom(msg.bebDeliver.message.appValue)

                msg_to_send.plSend.message.CopyFrom(inner_message)
            
            case pb.Message.Type.NNAR_WRITE_RETURN:
                # Create message for PL_SEND
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.Type.PL_SEND
                msg_to_send.FromAbstractionId = "app"
                msg_to_send.ToAbstractionId = "app.pl"

                # Create the inner message for APP_WRITE_RETURN
                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.APP_WRITE_RETURN

                # Extract register ID from the incoming message's abstraction ID
                register = utils.extract_register_id(msg.FromAbstractionId)
                inner_message.appWriteReturn.register = register

                # Set the inner message in PlSend
                msg_to_send.plSend.message.CopyFrom(inner_message)

            case pb.Message.Type.NNAR_READ_RETURN:
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.Type.PL_SEND
                msg_to_send.FromAbstractionId = "app"
                msg_to_send.ToAbstractionId = "app.pl"

                # Create inner message for PL_SEND
                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.APP_READ_RETURN
                inner_message.appReadReturn.register = utils.extract_register_id(msg.FromAbstractionId)
                inner_message.appReadReturn.value.CopyFrom(msg.nnarReadReturn.value)

                # Attach inner message to outer message
                msg_to_send.plSend.message.CopyFrom(inner_message)

            case pb.Message.Type.UC_DECIDE:
                # Create the outer message for PL_SEND
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.Type.PL_SEND
                msg_to_send.FromAbstractionId = "app" 
                msg_to_send.ToAbstractionId = "app.pl"

                # Create the inner message for APP_DECIDE
                inner_message = pb.Message()
                inner_message.type = pb.Message.Type.APP_DECIDE
                inner_message.ToAbstractionId = "app"

                # Copy the value from UcDecide to AppDecide
                inner_message.appDecide.value.CopyFrom(msg.ucDecide.value)

                # Set the inner message in PlSend
                msg_to_send.plSend.message.CopyFrom(inner_message)
        self.msg_queue.put(msg_to_send, block=False)
