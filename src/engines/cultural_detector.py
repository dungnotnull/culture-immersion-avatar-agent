import torch
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from typing import List, Dict, Any
from src.core.logger import logger
from src.core.config import settings
import numpy as np
from sentence_transformers import SentenceTransformer, util

class CulturalTermDetector:
    def __init__(self, keyword_dict: Dict[str, str] = None):
        self.keyword_dict = keyword_dict or {}
        logger.info(f"Initializing CulturalTermDetector with {len(self.keyword_dict)} keywords")
        
        # Load BERT NER Pipeline
        try:
            self.ner_pipeline = pipeline(
                "ner", 
                model=settings.NER_MODEL_NAME, 
                tokenizer=settings.NER_MODEL_NAME, 
                aggregation_strategy="simple"
            )
            logger.info("BERT NER pipeline loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load NER pipeline: {e}")
            self.ner_pipeline = None

        # Load Semantic Similarity Model
        try:
            self.similarity_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            logger.info("Semantic similarity model loaded.")
        except Exception as e:
            logger.error(f"Failed to load similarity model: {e}")
            self.similarity_model = None

    def detect(self, text: str) -> List[Dict[str, Any]]:
        """
        Detects cultural terms using a hybrid approach:
        1. Exact keyword match (High confidence)
        2. NER detection (Medium confidence)
        3. Semantic similarity to known cultural patterns (Low-Med confidence)
        """
        detected = []

        # 1. Keyword Match
        for term, meaning in self.keyword_dict.items():
            if term in text:
                detected.append({
                    "term": term, 
                    "type": "keyword", 
                    "confidence": 1.0, 
                    "context": meaning
                })

        # 2. NER Pipeline (Named Entity Recognition)
        if self.ner_pipeline:
            try:
                ner_results = self.ner_pipeline(text)
                for entity in ner_results:
                    # We treat PER, ORG, LOC and MISC as potential cultural markers
                    # in a foreign language context
                    detected.append({
                        "term": entity["word"],
                        "type": "NER",
                        "confidence": entity["score"],
                        "label": entity["entity_group"]
                    })
            except Exception as e:
                logger.error(f"NER detection failed: {e}")

        # 3. Semantic Similarity (Simplified)
        # In a production run, we would match against a 'Cultural Seed Set'
        # For now, we prioritize keywords and NER.

        # Deduplicate and filter by confidence
        unique_detected = self._deduplicate(detected)
        return unique_detected

    def _deduplicate(self, results: List[Dict]) -> List[Dict]:
        seen = {}
        for item in results:
            term = item["term"]
            conf = item["confidence"]
            if term not in seen or conf > seen[term]["confidence"]:
                seen[term] = item
        return list(seen.values())

    def add_keywords(self, keywords: Dict[str, str]):
        self.keyword_dict.update(keywords)
