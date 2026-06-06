import os
import pysrt
from typing import List
from src.engines.subtitle_engine import SubtitleEngine, SubtitleLine, SRTParser

class RealSRTParser(SRTParser):
    def parse(self, file_path: str) -> List[SubtitleLine]:
        subs = pysrt.open(file_path)
        return [
            SubtitleLine(
                start_time=float(s.start.ordinal), 
                end_time=float(s.end.ordinal), 
                text=s.text, 
                index=i
            ) for i, s in enumerate(subs)
        ]

# Patching the engine to use real parsers if libraries are present
def patch_subtitle_engine():
    import src.engines.subtitle_engine as se
    se.SubtitleEngine.parsers['.srt'] = RealSRTParser()
    # ASS and VTT would be patched similarly with python-ass and webvtt-py
