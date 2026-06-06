import asyncio
import requests
import json
from typing import Optional
from src.core.logger import logger

class TimestampSyncEngine:
    def __init__(self):
        self.current_timestamp = 0.0
        self.player_type = None # 'vlc', 'mpv', or None

    def set_player_type(self, player: str):
        self.player_type = player.lower()
        logger.info(f"Sync Engine configured for player: {self.player_type}")

    async def update_timestamp(self):
        """
        Polls the media player for the current playback position.
        """
        if self.player_type == 'vlc':
            await self._poll_vlc()
        elif self.player_type == 'mpv':
            await self._poll_mpv()
        else:
            # Linear simulation if no player is detected/configured
            self.current_timestamp += 0.1 

    async def _poll_vlc(self):
        try:
            # Default VLC RC port is 8080 or via HTTP interface
            response = requests.get("http://localhost:8080/requests.txt", timeout=0.1)
            # This is simplified; real VLC RC requires specific config and command parsing
            # Example: 'get_time' returns time in ms
            if response.status_code == 200:
                # Logic to extract time from VLC response
                pass 
        except Exception:
            pass

    async def _poll_mpv(self and socket_path="/tmp/mpv-socket"):
        try:
            # MPV uses a JSON IPC socket
            import socket
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(socket_path)
                s.sendall(b'{"command": "get_property", "params": ["time"]}\n')
                data = s.recv(1024)
                result = json.loads(data.decode())
                self.current_timestamp = result.get("data", 0.0)
        except Exception:
            pass

    def get_current_time(self) -> float:
        return self.current_timestamp
