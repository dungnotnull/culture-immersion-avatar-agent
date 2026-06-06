import asyncio
import time
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from src.core.logger import logger
from src.engines.subtitle_engine import SubtitleEngine
from src.engines.cultural_detector import CulturalTermDetector
from src.engines.llm_manager import LLMManager
from src.data.culture_cache import CultureCache
from src.engines.sync_engine import TimestampSyncEngine
from src.ui.overlay import CulturalOverlay

class CultureImmersionApp:
    def __init__(self):
        # Initialize PyQt Application
        self.app = QApplication(sys.argv)
        
        # Components
        self.overlay = CulturalOverlay()
        self.subtitle_engine = SubtitleEngine()
        self.detector = CulturalTermDetector()
        self.llm = LLMManager()
        self.cache = CultureCache()
        self.sync = TimestampSyncEngine()
        
        self.current_subs = []
        self.is_running = False
        self.last_processed_idx = -1

    async def initialize_backend(self):
        logger.info("Initializing backend services...")
        await self.cache.init_db()
        # In a real setup, we would load a keyword JSON here
        # self.detector.add_keywords(load_json("keywords.json"))

    def load_file(self, path: str):
        try:
            self.current_subs = self.subtitle_engine.load_subtitles(path)
            logger.info(f"Loaded {len(self.current_subs)} lines from {path}")
        except Exception as e:
            logger.error(f"Failed to load subtitles: {e}")

    async def main_loop(self):
        """
        The core async orchestration loop.
        """
        self.is_running = True
        logger.info("Starting main orchestration loop...")
        
        while self.is_running:
            # 1. Update playback time from player
            await self.sync.update_timestamp()
            current_time = self.sync.get_current_time()
            
            # 2. Find active subtitle line
            active_idx = self._find_active_line(current_time)
            
            # 3. Only process if we've hit a NEW line to avoid hammering the LLM/Cache
            if active_idx is not None and active_idx != self.last_processed_idx:
                line = self.current_subs[active_idx]
                await self.process_line(line)
                self.last_processed_idx = active_idx
            
            # Small sleep to prevent CPU spiking
            await asyncio.sleep(0.1)

    def _find_active_line(self, current_time: float) -> Optional[int]:
        for i, line in enumerate(self.current_subs):
            if line.start_time <= current_time <= line.end_time:
                return i
        return None

    async def process_line(self, line):
        logger.debug(f"Processing line {line.index}: {line.text}")
        
        # Detect cultural terms
        terms = self.detector.detect(line.text)
        
        for item in terms:
            term = item['term']
            
            # Check cache first
            explanation = await self.cache.get(term, "en")
            
            if not explanation:
                logger.info(f"Cache miss for '{term}'. Requesting LLM explanation...")
                explanation = await self.llm.get_explanation(term, line.text)
                await self.cache.set(term, "en", explanation)
            
            # Trigger UI overlay
            self.overlay.show_note(term, explanation)

    def run(self):
        # Setup async bridge for PyQt
        loop = asyncio.get_event_loop()
        
        # Initialize cache
        loop.run_until_complete(self.initialize_backend())
        
        # Start the main orchestration loop in the background
        asyncio.ensure_future(self.main_loop())
        
        # Start PyQt event loop
        self.app.exec()

if __name__ == "__main__":
    app = CultureImmersionApp()
    # Replace with a real path to a subtitle file for testing
    app.load_file("test.srt") 
    app.run()
