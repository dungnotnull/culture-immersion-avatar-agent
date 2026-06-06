import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from src.core.config import settings
from src.core.logger import logger

class CulturalOverlay(QWidget):
    # Signal to update text from the main async thread
    update_text_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_text_signal.connect(self.on_update_text)

    def init_ui(self):
        # Make window transparent, frameless, and always on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.label = QLabel("Waiting for cultural terms...")
        
        # High-quality editorial style
        self.label.setStyleSheet(f"""
            QLabel {{
                color: #FFFFFF; 
                font-size: 18px; 
                background-color: rgba(20, 20, 20, 180); 
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 12px; 
                padding: 15px;
                font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            }}
            b {{ color: #FFD700; font-size: 20px; }}
        """)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        
        self.setWindowOpacity(settings.OVERLAY_OPACITY)
        self.resize(450, 180)
        self.move(100, 100) 

    @pyqtSlot(str, str)
    def on_update_text(self, term: str, explanation: str):
        logger.info(f"Overlay displaying: {term}")
        self.label.setText(f"<b>{term}</b><br><br>{explanation}")
        self.show()
        
        # Auto-dismiss timer
        QTimer.singleShot(settings.OVERLAY_DURATION * 1000, self.hide)

    def show_note(self, term: str, explanation: str):
        # This method allows the main app to trigger the signal
        self.update_text_signal.emit(term, explanation)
