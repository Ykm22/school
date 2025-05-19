import threading
from pb import communication_protocol_pb2 as pb
from util.log import debug, info, error

class System:
    def __init__(self, system_id, owner, index, port, host, hub_address):
        """
        Initialize a new system.
        
        Parameters:
            system_id (str): The ID of the system
            owner (str): Owner alias
            index (int): Process index
            port (int): Listening port
            host (str): Host address
            hub_address (str): Hub address (host:port)
        """
        self.system_id = system_id
        self.owner = owner
        self.index = index
        self.port = port
        self.host = host
        self.hub_address = hub_address
        self.abstractions = {}  # Map of abstraction_id to abstraction instance
        self.message_queue = []
        self.processes = []
        self.own_process = None
        self.running = False
        self.thread = None
        self.lock = threading.Lock()
        
    def initialize(self, processes):
        """
        Initialize the system with the given processes.
        
        Parameters:
            processes (list): List of ProcessId instances
        """
        self.processes = processes
        
        # Find our own process in the list
        for process in processes:
            if process.owner == self.owner and process.index == self.index:
                self.own_process = process
                break
                
        if not self.own_process:
            error(f"Could not find own process in the list of processes")
            return
            
        # Initialize the basic abstractions
        self.register_abstractions()
        
        # Start processing messages
        self.running = True
        self.thread = threading.Thread(target=self._process_messages)
        self.thread.daemon = True
        self.thread.start()
        
        info(f"System {self.system_id} initialized with {len(processes)} processes")
    
    def register_abstractions(self):
        """Register the initial abstractions such as app, beb, pl"""
        from pl.perfect_link import PerfectLink  # Import here to avoid circular imports
        
        # Create perfect link
        pl = PerfectLink(self.host, self.port, self.hub_address, self.system_id, self.processes)
        
        # Import other abstractions here to avoid circular imports
        from app.app import App
        from broadcast.beb import BestEffortBroadcast
        
        # Register app and its pl
        self.abstractions["app"] = App(self.message_queue)
        self.abstractions["app.pl"] = pl
        
        # Register beb and its pl
        self.abstractions["app.beb"] = BestEffortBroadcast(self.message_queue, self.processes, "app.beb")
        self.abstractions["app.beb.pl"] = pl.copy_with_parent("app.beb")
        
    def register_nnar_abstractions(self, key):
        """
        Register abstractions for N,N Atomic Register.
        
        Parameters:
            key (str): Register key
        """
        from pl.perfect_link import PerfectLink
        from broadcast.beb import BestEffortBroadcast
        from register.nnar import NnAtomicRegister
        
        abstraction_id = f"app.nnar[{key}]"
        
        if abstraction_id not in self.abstractions:
            info(f"Registering abstractions for {abstraction_id}")
            
            pl = PerfectLink(self.host, self.port, self.hub_address, self.system_id, self.processes)
            
            # Create atomic register
            self.abstractions[abstraction_id] = NnAtomicRegister(
                self.message_queue,
                len(self.processes),
                key,
                self.own_process.rank
            )
            
            # Register necessary abstractions
            self.abstractions[f"{abstraction_id}.pl"] = pl.copy_with_parent(abstraction_id)
            self.abstractions[f"{abstraction_id}.beb"] = BestEffortBroadcast(
                self.message_queue, 
                self.processes, 
                f"{abstraction_id}.beb"
            )
            self.abstractions[f"{abstraction_id}.beb.pl"] = pl.copy_with_parent(f"{abstraction_id}.beb")
    
    def handle_message(self, message):
        """
        Handle an incoming message.
        
        Parameters:
            message (Message): The message to handle
        """
        # Add message to queue
        with self.lock:
            self.message_queue.append(message)
        
        debug(f"Added message of type {message.type} to queue for abstraction {message.ToAbstractionId}")
    
    def _process_messages(self):
        """Process messages from the queue"""
        while self.running:
            # Get next message
            message = None
            with self.lock:
                if self.message_queue:
                    message = self.message_queue.pop(0)
            
            if not message:
                # If no messages, sleep briefly
                import time
                time.sleep(0.01)
                continue
            
            # Check if we need to create NNAR abstractions
            if message.ToAbstractionId.startswith("app.nnar[") and message.ToAbstractionId not in self.abstractions:
                key = message.ToAbstractionId[len("app.nnar["):-1]  # Extract key from abstraction ID
                self.register_nnar_abstractions(key)
            
            # Find the abstraction to handle this message
            abstraction = self.abstractions.get(message.ToAbstractionId)
            if abstraction:
                try:
                    abstraction.handle(message)
                except Exception as e:
                    error(f"Error handling message type {message.type}: {e}")
            else:
                error(f"No abstraction registered for {message.ToAbstractionId}")
    
    def destroy(self):
        """Destroy the system and clean up resources"""
        self.running = False
        
        # Wait for thread to finish
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        
        # Clean up abstractions
        for abstraction_id, abstraction in self.abstractions.items():
            if hasattr(abstraction, 'destroy'):
                try:
                    abstraction.destroy()
                except Exception as e:
                    error(f"Error destroying abstraction {abstraction_id}: {e}")
        
        self.abstractions.clear()
        info(f"System {self.system_id} destroyed")
