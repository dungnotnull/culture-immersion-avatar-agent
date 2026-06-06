import abc
from typing import List, Dict, Optional
from src.core.logger import logger

class CulturalTermDetector:
    def __init__(self, keyword_dict: Optional[Dict[str, str]] = None):
        self.keyword_dict = keyword_dict or {}
        self.ner_model = None # Mocked: would be dslim/bert-base-NER pipeline

    def detect(self, text: str) -> List[Dict]:
        """
        Detects cultural terms using keyword lookup and (mocked) NER.
        Returns a list of detected terms with their metadata.
        """
        detected = []
        
        # 1. Keyword Lookup
        for term, meaning in self.keyword_dict.items():
            if term in text:
                detected.append({"term": term, "type": "keyword", "confidence": 1.0})
        
        # 2. Mocked NER
        # In real run: results = self.ner_model(text)
        if "culture" in text.lower(): # Simulation for Phase 0
            detected.append({"term": "mock_cultural_entity", "type": "NER", "confidence": 0.8})
            
        return detected
