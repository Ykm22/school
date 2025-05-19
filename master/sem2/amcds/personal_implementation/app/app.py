from pb import communication_protocol_pb2 as pb
from util.log import debug, info, error

class App:
    """
    Application abstraction.
    Handles application-level messages.
    """
    
    def __init__(self, message_queue):
        """
        Initialize a new App.
        
        Parameters:
            message_queue: Shared message queue
        """
        self.message_queue = message_queue
    
    def handle(self, message):
        """
        Handle an incoming message.
        
        Parameters:
            message (Message): The message to handle
            
        Returns:
            bool: True if handled successfully, False otherwise
        """
        msg_to_send = None
        
        if message.type == pb.Message.PL_DELIVER:
            inner_message = message.plDeliver.message
            
            if inner_message.type == pb.Message.APP_BROADCAST:
                # Handle broadcast request
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.BEB_BROADCAST
                msg_to_send.systemId = message.systemId
                msg_to_send.FromAbstractionId = "app"
                msg_to_send.ToAbstractionId = "app.beb"
                
                # Create APP_VALUE message
                value_msg = pb.Message()
                value_msg.type = pb.Message.APP_VALUE
                value_msg.FromAbstractionId = "app"
                value_msg.ToAbstractionId = "app"
                value_msg.appValue.value.CopyFrom(inner_message.appBroadcast.value)
                
                msg_to_send.bebBroadcast.message.CopyFrom(value_msg)
                
            elif inner_message.type == pb.Message.APP_VALUE:
                # Handle APP_VALUE message - forward to hub
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.PL_SEND
                msg_to_send.systemId = message.systemId
                msg_to_send.FromAbstractionId = "app"
                msg_to_send.ToAbstractionId = "app.pl"
                
                # Forward the APP_VALUE message
                app_value_msg = pb.Message()
                app_value_msg.type = pb.Message.APP_VALUE
                app_value_msg.appValue.value.CopyFrom(inner_message.appValue.value)
                
                msg_to_send.plSend.message.CopyFrom(app_value_msg)
                
            elif inner_message.type == pb.Message.APP_WRITE:
                # Handle APP_WRITE message - forward to NNAR
                register_id = inner_message.appWrite.register
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.NNAR_WRITE
                msg_to_send.systemId = message.systemId
                msg_to_send.FromAbstractionId = "app"
                msg_to_send.ToAbstractionId = f"app.nnar[{register_id}]"
                
                # Copy the value to write
                msg_to_send.nnarWrite.value.CopyFrom(inner_message.appWrite.value)
                
            elif inner_message.type == pb.Message.APP_READ:
                # Handle APP_READ message - forward to NNAR
                register_id = inner_message.appRead.register
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.NNAR_READ
                msg_to_send.systemId = message.systemId
                msg_to_send.FromAbstractionId = "app"
                msg_to_send.ToAbstractionId = f"app.nnar[{register_id}]"
                
        elif message.type == pb.Message.BEB_DELIVER:
            # Handle delivery from BEB - forward to hub
            if message.bebDeliver.message.type == pb.Message.APP_VALUE:
                msg_to_send = pb.Message()
                msg_to_send.type = pb.Message.PL_SEND
                msg_to_send.systemId = message.systemId
                msg_to_send.FromAbstractionId = "app"
                msg_to_send.ToAbstractionId = "app.pl"
                
                # Create APP_VALUE message
                app_value_msg = pb.Message()
                app_value_msg.type = pb.Message.APP_VALUE
                app_value_msg.appValue.value.CopyFrom(message.bebDeliver.message.appValue.value)
                
                msg_to_send.plSend.message.CopyFrom(app_value_msg)
                
                # Log the delivered value
                value = message.bebDeliver.message.appValue.value
                if value.defined:
                    info(f"Delivered value: {value.v}")
                else:
                    info("Delivered undefined value")
                
        elif message.type == pb.Message.NNAR_WRITE_RETURN:
            # Handle write confirmation - forward to hub
            register_id = message.FromAbstractionId.split('[')[1].rstrip(']')
            
            msg_to_send = pb.Message()
            msg_to_send.type = pb.Message.PL_SEND
            msg_to_send.systemId = message.systemId
            msg_to_send.FromAbstractionId = "app"
            msg_to_send.ToAbstractionId = "app.pl"
            
            # Create APP_WRITE_RETURN message
            write_return_msg = pb.Message()
            write_return_msg.type = pb.Message.APP_WRITE_RETURN
            write_return_msg.appWriteReturn.register = register_id
            
            msg_to_send.plSend.message.CopyFrom(write_return_msg)
            
            info(f"Finished writing to register '{register_id}'")
            
        elif message.type == pb.Message.NNAR_READ_RETURN:
            # Handle read result - forward to hub
            register_id = message.FromAbstractionId.split('[')[1].rstrip(']')
            
            msg_to_send = pb.Message()
            msg_to_send.type = pb.Message.PL_SEND
            msg_to_send.systemId = message.systemId
            msg_to_send.FromAbstractionId = "app"
            msg_to_send.ToAbstractionId = "app.pl"
            
            # Create APP_READ_RETURN message
            read_return_msg = pb.Message()
            read_return_msg.type = pb.Message.APP_READ_RETURN
            read_return_msg.appReadReturn.register = register_id
            read_return_msg.appReadReturn.value.CopyFrom(message.nnarReadReturn.value)
            
            msg_to_send.plSend.message.CopyFrom(read_return_msg)
            
            # Log the read value
            value = message.nnarReadReturn.value
            if value.defined:
                info(f"Read value from register '{register_id}': {value.v}")
            else:
                info(f"Read undefined value from register '{register_id}'")
        
        # Send the message if created
        if msg_to_send:
            self.message_queue.append(msg_to_send)
            return True
            
        return False
    
    def destroy(self):
        """Clean up resources"""
        # No resources to clean up
        pass
