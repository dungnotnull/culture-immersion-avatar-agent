import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from src.core.config import settings
from src.core.logger import logger

class CulturalOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Make window transparent and always on top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        self.label = QLabel("Waiting for cultural terms...")
        self.label.setStyleSheet("color: white; font-size: 18px; background-color: rgba(0, 0, 0, 150); border-radius: 10px; padding: 10px;")
        self.label.setWordWrap(True)
        
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        
        self.setWindowOpacity(settings.OVERLAY_OPACITY)
        self.resize(400, 150)
        self.move(100, 100) # Default position

    def show_note(self, term: str, explanation: str):
        logger.info(f"Overlay showing: {term}")
        self.label.setText(f"<b>{term}</b><br>{explanation}")
        self.show()
        
        # Auto-dismiss timer
        QTimer.singleShot(settings.OVERLAY_DURATION * 1000, self.hide)

if __name__ == "__main__":
    # Simple test run
    app = QApplication(sys.argv)
    overlay = CulturalOverlay()
    overlay.show_note("Kuuki Yomu", "Reading the air: the Japanese art of sensing the mood and unspoken thoughts.")
    sys.exit(app.exec())
