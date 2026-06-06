from dataclasses import dataclass
from typing import Optional
from src.core.logger import logger

@dataclass
class SyncState:
    current_timestamp: float = 0.0
    active_line_index: Optional[int] = None

class TimestampSyncEngine:
    def __init__(self):
        self.state = SyncState()

    def update_timestamp(self, timestamp: float):
        self.state.current_timestamp = timestamp
        # logger.debug(f"Sync Engine: {timestamp:.2f}s")

    def get_active_line(self, subtitles) -> Optional[int]:
        # subtitles is a list of SubtitleLine objects
        for i, line in enumerate(subtitles):
            if line.start_time <= self.state.current_timestamp <= line.end_time:
                return i
        return None
