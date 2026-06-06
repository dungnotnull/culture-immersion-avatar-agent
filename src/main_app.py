import time
from src.core.logger import logger
from src.engines.subtitle_engine import SubtitleEngine
from src.engines.cultural_detector import CulturalTermDetector
from src.engines.llm_manager import LLMManager
from src.data.culture_cache import CultureCache
from src.engines.sync_engine import TimestampSyncEngine
from src.ui.overlay import CulturalOverlay
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

class CultureImmersionApp:
    def __init__(self):
        self.app = QApplication([])
        self.overlay = CulturalOverlay()
        self.subtitle_engine = SubtitleEngine()
        self.detector = CulturalTermDetector()
        self.llm = LLMManager()
        self.cache = CultureCache()
        self.sync = TimestampSyncEngine()
        
        self.current_subs = []
        self.is_running = False

    def load_file(self, path: str):
        self.current_subs = self.subtitle_engine.load_subtitles(path)
        logger.info(f"Loaded {len(self.current_subs)} lines from {path}")

    def tick(self):
        if not self.is_running: return
        
        # Simulate getting current time from media player (Mocked as linear progression)
        current_time = time.time() % 3600 
        self.sync.update_timestamp(current_time)
        
        idx = self.sync.get_active_line(self.current_subs)
        if idx is not None:
            line = self.current_subs[idx]
            self.process_line(line)

    def process_line(self, line):
        terms = self.detector.detect(line.text)
        for item in terms:
            term = item['term']
            explanation = self.cache.get(term, "en")
            if not explanation:
                explanation = self.llm.get_explanation(term, line.text)
                self.cache.set(term, "en", explanation)
            
            self.overlay.show_note(term, explanation)

    def run(self):
        self.is_running = True
        timer = QTimer()
        timer.timeout.connect(self.tick)
        timer.start(100) # 10Hz check
        self.app.exec()

if __name__ == "__main__":
    app = CultureImmersionApp()
    app.load_file("test.srt")
    app.run()
