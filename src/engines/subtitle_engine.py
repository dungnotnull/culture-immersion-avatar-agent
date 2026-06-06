import abc
from dataclasses import dataclass
from typing import List, Optional
import os
import pysrt
import ass
import webvtt_py
from src.core.logger import logger

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
        try:
            subs = pysrt.open(file_path)
            return [
                SubtitleLine(
                    start_time=s.start.ordinal / 1000.0,
                    end_time=s.end.ordinal / 1000.0,
                    text=s.text,
                    index=s.index
                ) for s in subs
            ]
        except Exception as e:
            logger.error(f"SRT parsing error: {e}")
            return []

class ASSParser(SubtitleParser):
    def parse(self, file_path: str) -> List[SubtitleLine]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = ass.load(f.read())
            
            lines = []
                # ASS files have a different structure; we flatten to simple lines
            for i, event in enumerate(data.events):
                # Convert ASS time format (H:MM:SS,mmm) to seconds
                start = self._parse_ass_time(event.start)
                end = self._parse_ass_time(event.end)
                # Remove formatting tags like {\pos(x,y)}
                text = self._strip_ass_tags(event.text)
                lines.append(SubtitleLine(start, end, text, i))
            return lines
        except Exception as e:
            logger.error(f"ASS parsing error: {e}")
            return []

    def _parse_ass_time(self, time_str: str) -> float:
        # H:MM:SS.mmm
        parts = time_str.split(':')
        h = float(parts[0])
        m = float(parts[1])
        s = float(parts[2])
        return h * 3600 + m * 60 + s

    def _strip_ass_tags(self, text: str) -> str:
        import re
        return re.sub(r'\{.*?\}', '', text).replace(r'\N', r'\n').replace(r'\h', ' ')

class VTTParser(SubtitleParser):
    def parse(self, file_path: str) -> List[SubtitleLine]:
        try:
            vtt = webvtt_py.Reader()
            subs = vtt.read(file_path)
            return [
                SubtitleLine(
                    start_time=float(s.start),
                    end_time=float(s.end),
                    text=s.text,
                    index=i
                ) for i, s in enumerate(subs)
            ]
        except Exception as e:
            logger.error(f"VTT parsing error: {e}")
            return []

class SubtitleEngine:
    def __init__(self):
        self.parsers = {
            '.srt': SRTParser(),
            '.ass': ASSParser(),
            '.vtt': VTTParser()
        }

    def load_subtitles(self, file_path: str) -> List[SubtitleLine]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Subtitle file not found: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        parser = self.parsers.get(ext)
        if not parser:
            raise ValueError(f"Unsupported subtitle format: {ext}")
            
        logger.info(f"Parsing subtitle file: {file_path} using {parser.__class__.__name__}")
        return parser.parse(file_path)
