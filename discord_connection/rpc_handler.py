import os
import sys

from pypresence.presence import Presence
import time


class DiscordRPCHandler:
    rpc = None
    def __init__(self, client_id):
        self.rpc = Presence(client_id)
        while True:
            try:
                self.rpc.connect()
                print("Connected to Discord RPC!")
                break
            except Exception as e:
                print(f"Failed to connect via RPC: {e}.")
                time.sleep(5)

    def sigint_handler(self, signum, frame):
        payload = {
                    "cmd": "SET_ACTIVITY",
                    "args": {"pid": os.getpid(), "activity": None},
                    "nonce": "c",
                }
        try:
            self.rpc.update(payload_override=payload)
        except:
            if self.rpc:
                try:
                    self.rpc.close()
                except:
                    pass
        sys.exit(0)
    
    def is_connected(self): 
        # pypresence doesn't provide a built-in way to check connection status
        # instead we just check if the rpc object exists.
        return self.rpc is not None
        
    def disconnect(self):
        if self.rpc:
            try:
                self.rpc.close()
            except:
                pass
 
    def update_presence(self, activity):
        if self.rpc:
            try:
                payload = {
                "cmd": "SET_ACTIVITY",
                "args": {"pid": os.getpid(), "activity": activity},
                "nonce": str(time.time()),
            }
                self.rpc.update(payload_override=payload)
            except Exception as e:
                print(f"Error updating RPC presence: {e}")