import argparse
from pl.perfect_link import PerfectLink
import pb.communication_protocol_pb2 as pb
import time
from tcp import tcp
from system.system import System

systems = {}

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process hub and process information.')
    
    parser.add_argument('hub_ip', help='IP address of the hub')
    parser.add_argument('hub_port', type=int, help='Port of the hub')
    parser.add_argument('owner', help='Owner identifier')
    parser.add_argument('host', help='IP address for processes')
    parser.add_argument('process_ports', type=int, nargs='+', help='Ports for processes (one or more)')
    
    return parser.parse_args()

def register(pl: PerfectLink, owner: str, destination_host: str, destination_port: str) -> bool:
    try:
        msg = pb.Message()
        msg.type = pb.Message.Type.PL_SEND
        
        # Set the destination
        msg.plSend.destination.host = destination_host
        msg.plSend.destination.port = int(destination_port)
        
        # Set the registration message
        msg.plSend.message.type = pb.Message.Type.PROC_REGISTRATION
        msg.plSend.message.procRegistration.owner = owner
        msg.plSend.message.procRegistration.index = 1
        
        success = pl.handle(msg)
        if not success:
            print("Registration message failed to send")
        return success
    except Exception as e:
        print(f"Error registering process: {str(e)}")
        return False


def message_handler(data: bytes, hub_ip: str, hub_port: str, host_ip: str, host_port: str, owner: str, idx: int):
    try:
        msg = pb.Message()
        msg.ParseFromString(data)
        
        print(f"Received message of type: {msg.type}")
        # print(msg)

        if msg.type == pb.Message.Type.NETWORK_MESSAGE:
            system_id = msg.systemId
            match msg.networkMessage.message.type:
                case pb.Message.Type.PROC_DESTROY_SYSTEM:
                    print("this should destroy system")
                case pb.Message.Type.PROC_INITIALIZE_SYSTEM:
                    print("this should init system")
                    system = System(host_ip, host_port, owner, idx, 
                                    hub_ip, hub_port, 
                                    msg.networkMessage.message)
                    systems[system_id] = system
                case _:
                    inner_message = msg.networkMessage.message
                    print(f"Default case, inner message type: {inner_message.type}")
                    if system_id in systems:
                        systems[system_id].add_message(msg)
                    else:
                        print(f"System {system_id} not initialized")

        
    except Exception as e:
        print(f"Error processing message: {str(e)}")

def main():
    args = parse_arguments()

    pl = PerfectLink(args.host, args.process_ports[0], args.hub_ip, args.hub_port)

    if not register(pl, args.owner, args.hub_ip, args.hub_port):
        return

    listener = tcp.listen(args.host, args.process_ports[0], 
        lambda data: message_handler(data, 
                                     args.hub_ip, args.hub_port, 
                                     args.host, args.process_ports[0], args.owner, 1
        )
    )

    try:
        print("Server running. Press Ctrl+C to stop.")
        while True:
            # Your main program logic here
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        # Clean up
        if listener:
            listener.close()


    print("upii")


if __name__ == "__main__":
    main()
