import abc
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SubtitleLine:
    start_time: float  # seconds
    end_time: float    # seconds
    text: str
    index: int

class SubtitleParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, file_path: str) -> List[SubtitleLine]:
        pass

class SRTParser(SubtitleParser):
    def parse(self, file_path: str) -> List[SubtitleLine]:
        # TODO: Implement real pysrt logic
        return [SubtitleLine(0.0, 2.0, "Mock SRT Text", 1)]

class ASSParser(SubtitleParser):
    def parse(self, file_path: str) -> List[SubtitleLine]:
        # TODO: Implement real python-ass logic
        return [SubtitleLine(0.0, 2.0, "Mock ASS Text", 1)]

class VTTParser(SubtitleParser):
    def parse(self, file_path: str) -> List[SubtitleLine]:
        # TODO: Implement real webvtt-py logic
        return [SubtitleLine(0.0, 2.0, "Mock VTT Text", 1)]

class SubtitleEngine:
    def __init__(self):
        self.parsers = {
            '.srt': SRTParser(),
            '.ass': ASSParser(),
            '.vtt': VTTParser()
        }

    def load_subtitles(self, file_path: str) -> List[SubtitleLine]:
        import os
        ext = os.path.splitext(file_path)[1].lower()
        parser = self.parsers.get(ext)
        if not parser:
            raise ValueError(f"Unsupported subtitle format: {ext}")
        return parser.parse(file_path)
