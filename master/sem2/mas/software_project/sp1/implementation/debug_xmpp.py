#!/usr/bin/env python3
"""
XMPP Server Debug Script
This script helps debug XMPP server connectivity and user registration.
"""

import asyncio
import logging
from spade.agent import Agent

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAgent(Agent):
    async def setup(self):
        logger.info(f"Test agent {self.jid} connected successfully!")

async def test_connection():
    """Test XMPP server connection and user registration."""
    
    logger.info("=== XMPP Server Connection Test ===")
    
    # Test configurations
    test_configs = [
        {"jid": "pacman@localhost", "password": "password"},
        {"jid": "environment@localhost", "password": "password"},
        {"jid": "admin@localhost", "password": "admin"},
    ]
    
    for config in test_configs:
        jid = config["jid"]
        password = config["password"]
        
        logger.info(f"Testing connection for {jid}...")
        
        agent = TestAgent(jid, password)
        
        try:
            # Try with auto-register first
            logger.info(f"  -> Attempting auto-register for {jid}")
            await agent.start(auto_register=True)
            logger.info(f"  ✅ SUCCESS: {jid} connected with auto-register")
            await agent.stop()
            
        except Exception as e:
            logger.error(f"  ❌ FAILED auto-register for {jid}: {e}")
            
            try:
                # Try without auto-register
                logger.info(f"  -> Attempting normal connection for {jid}")
                await agent.start(auto_register=False)
                logger.info(f"  ✅ SUCCESS: {jid} connected normally")
                await agent.stop()
                
            except Exception as e2:
                logger.error(f"  ❌ FAILED normal connection for {jid}: {e2}")
        
        await asyncio.sleep(1)  # Small delay between tests

async def check_server_status():
    """Check if XMPP server is reachable."""
    import socket
    
    logger.info("=== Server Reachability Test ===")
    
    host = "localhost"
    ports = [5222, 5280, 5443]
    
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                logger.info(f"  ✅ Port {port} is OPEN")
            else:
                logger.error(f"  ❌ Port {port} is CLOSED")
        except Exception as e:
            logger.error(f"  ❌ Port {port} test failed: {e}")

async def main():
    """Main debug function."""
    
    print("🔧 SPADE/XMPP Debug Tool")
    print("=" * 50)
    
    # Check server reachability first
    await check_server_status()
    
    print()
    
    # Test agent connections
    await test_connection()
    
    print()
    print("=== Debug Complete ===")
    print("If all tests fail, check:")
    print("1. Docker container is running: docker ps")
    print("2. Docker logs: docker logs pacman_ejabberd")
    print("3. Port conflicts: netstat -tlnp | grep 5222")

if __name__ == "__main__":
    asyncio.run(main())
