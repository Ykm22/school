import argparse
import socket
import signal
import sys
import os
from concurrent.futures import ThreadPoolExecutor

from pb import communication_protocol_pb2 as pb
from system.system import System
from util.log import setup_logger, info, fatal, debug

# Global variables
systems = {}  # Map of system_id to System instance
logger = None


def register(owner, index, host, port, hub_address):
    """Register the process with the hub"""
    hub_host, hub_port = hub_address.split(':')
    
    message = pb.Message()
    message.type = pb.Message.PROC_REGISTRATION
    message.procRegistration.owner = owner
    message.procRegistration.index = index
    
    # Create network message wrapper
    network_message = pb.Message()
    network_message.type = pb.Message.NETWORK_MESSAGE
    network_message.networkMessage.senderHost = host
    network_message.networkMessage.senderListeningPort = port
    network_message.networkMessage.message.CopyFrom(message)
    
    # Send registration to hub
    send_message(hub_host, int(hub_port), network_message.SerializeToString())
    info(f"{owner}-{index} registered with hub at {hub_address}")

def send_message(host, port, data):
    """Send a message to the specified host and port"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            # First send the message size (4 bytes)
            size = len(data)
            size_bytes = size.to_bytes(4, byteorder='big')
            s.sendall(size_bytes + data)
    except Exception as e:
        debug(f"Failed to send message: {e}")

def receive_message(conn):
    """Receive a message from the given connection"""
    try:
        # Read message size (first 4 bytes)
        size_bytes = conn.recv(4)
        if not size_bytes or len(size_bytes) < 4:
            return None
            
        size = int.from_bytes(size_bytes, byteorder='big')
        data = conn.recv(size)
        
        if len(data) < size:
            # Handle partial reads if needed
            remaining = size - len(data)
            while remaining > 0:
                chunk = conn.recv(remaining)
                if not chunk:
                    break
                data += chunk
                remaining -= len(chunk)
                
        return data
    except Exception as e:
        debug(f"Error receiving message: {e}")
        return None

def handle_connection(conn, addr):
    """Handle incoming connection"""
    data = receive_message(conn)
    if data:
        message = pb.Message()
        message.ParseFromString(data)
        
        if message.type == pb.Message.NETWORK_MESSAGE:
            process_network_message(message)
        else:
            debug(f"Received non-network message: {message.type}")
    
    conn.close()

def process_network_message(message):
    """Process a network message"""
    inner_message = message.networkMessage.message
    
    if inner_message.type == pb.Message.PROC_INITIALIZE_SYSTEM:
        system_id = inner_message.systemId
        debug(f"Initializing system {system_id}")
        
        # Create a new system if it doesn't exist
        if system_id not in systems:
            systems[system_id] = System(system_id, args.owner, args.index, args.port, args.host, args.hub)
            systems[system_id].initialize(inner_message.procInitializeSystem.processes)
            
    elif inner_message.type == pb.Message.PROC_DESTROY_SYSTEM:
        system_id = inner_message.systemId
        if system_id in systems:
            debug(f"Destroying system {system_id}")
            systems[system_id].destroy()
            del systems[system_id]
            
    elif inner_message.systemId in systems:
        # Forward message to the appropriate system
        systems[inner_message.systemId].handle_message(inner_message)
    else:
        debug(f"Message for unknown system: {inner_message.systemId}")

def start_server(host, port):
    """Start the TCP server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(100)  # Allow up to 100 connections in the queue
        info(f"Listening on {host}:{port}")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                conn, addr = server_socket.accept()
                executor.submit(handle_connection, conn, addr)
                
    except KeyboardInterrupt:
        info("Server shutting down...")
    finally:
        server_socket.close()

def setup_signal_handlers():
    """Set up signal handlers for graceful shutdown"""
    def signal_handler(sig, frame):
        info("Shutting down...")
        # Clean up systems
        for system_id in list(systems.keys()):
            if systems[system_id]:
                systems[system_id].destroy()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def main():
    global args, logger
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AMCDS Process')
    parser.add_argument('-owner', default='user', help='Owner alias of the process')
    parser.add_argument('-hub', default='127.0.0.1:5000', help='Hub address (host:port)')
    parser.add_argument('-port', type=int, default=5004, help='Port to listen on')
    parser.add_argument('-index', type=int, default=1, help='Process index')
    parser.add_argument('-host', default='127.0.0.1', help='Host to bind to')
    
    args = parser.parse_args()
    
    # Setup logging
    # can add as argument log_file="./path/" for file output
    logger = setup_logger()
    
    # Setup signal handlers
    setup_signal_handlers()
    
    # Register with hub
    register(args.owner, args.index, args.host, args.port, args.hub)
    
    # Start listening for messages
    start_server(args.host, args.port)

if __name__ == "__main__":
    main()
