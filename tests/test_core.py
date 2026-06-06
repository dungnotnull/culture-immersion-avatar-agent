import pytest
from src.engines.subtitle_engine import SubtitleEngine, SubtitleLine

def test_subtitle_parsing():
    engine = SubtitleEngine()
    # Mock the parser since we aren't using real files in CI
    lines = engine.load_subtitles("mock.srt")
    assert len(lines) > 0
    assert isinstance(lines[0], SubtitleLine)

def test_sync_engine():
    from src.engines.sync_engine import TimestampSyncEngine
    sync = TimestampSyncEngine()
    subs = [SubtitleLine(1.0, 2.0, "Hello", 0)]
    sync.update_timestamp(1.5)
    assert sync.get_active_line(subs) == 0
    sync.update_timestamp(3.0)
    assert sync.get_active_line(subs) is None
