import pb.communication_protocol_pb2 as pb
import socket
import struct
import threading
from typing import Callable, Any

def send(address_ip: str, address_port: str, data: bytes):
    # print(data)
    # msg = pb.Message()
    # msg.ParseFromString(data)
    # print(msg)
    # print("hii")

    # Parse the address
    host = address_ip
    port = int(address_port)
    # print(f"sending to {host}:{port}")
    
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)  # Set a timeout of 5 seconds
        sock.connect((host, port))
        
        # Create a 4-byte length prefix in big-endian format
        length_bytes = struct.pack('>I', len(data))
        
        # Send the length followed by the data
        sock.sendall(length_bytes + data)
        return True  # Successful send
    except ConnectionRefusedError:
        print(f"Connection refused at {host}:{port}")
        return False
    except socket.timeout:
        print(f"Connection timed out at {host}:{port}")
        return False
    except Exception as e:
        print(f"Error sending data: {str(e)}")
        return False
    finally:
        if sock:
            sock.close()

def listen(address_ip: str, address_port: str, handler: Callable[[bytes], Any]) -> socket.socket:
    """
    Start a TCP server that listens for incoming messages and processes them with the handler.
    
    Args:
        address_ip: The IP address to listen on
        address_port: The port to listen on
        handler: A function that will be called with the received data
        
    Returns:
        The listener socket object
    """
    host = address_ip
    port = int(address_port)
    
    # Create and bind the server socket
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        listener.bind((host, port))
        listener.listen(5)
        print(f"Listening on {host}:{port}")
        
        def accept_connections():
            while True:
                try:
                    conn, addr = listener.accept()
                    try:
                        size_buf = conn.recv(4)
                        if len(size_buf) != 4:
                            print("Failed to read message size")
                            continue
 
                        # parse size as a big-endian uint32
                        message_size = struct.unpack('>I', size_buf)[0]

                        # Read exactly message_size bytes
                        data = b''
                        remaining = message_size
                        while remaining > 0:
                            chunk = conn.recv(min(4096, remaining))
                            if not chunk:
                                break
                            data += chunk
                            remaining -= len(chunk)

                        if len(data) != message_size:
                            print(f"Incomplete message: got {len(data)} bytes, expected {message_size}")
                            continue

                        # Pass the data to the handler
                        handler(data)

                    except Exception as e:
                        print(f"Error handling connection from {addr}: {str(e)}")
                    finally:
                        conn.close()

                except Exception as e:
                    # Check if the listener was closed
                    if listener.fileno() == -1:
                        break
                    print(f"Error accepting connection: {str(e)}")
        
        # Start the accept thread
        thread = threading.Thread(target=accept_connections)
        thread.daemon = True
        thread.start()
        
        return listener
        
    except Exception as e:
        print(f"Error setting up listener on {host}:{port}: {str(e)}")
        listener.close()
        raise
