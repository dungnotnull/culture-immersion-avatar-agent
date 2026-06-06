from typing import Dict, List
import json
import os

class SeriesMemory:
    def __init__(self, memory_file: str = "data/series_memory.json"):
        self.memory_file = memory_file
        self.memory = self._load()

    def _load(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        return {"entities": {}, "plot_points": [], "cultural_themes": []}

    def add_entity(self, entity: str, description: str):
        self.memory["entities"][entity] = description
        self._save()

    def get_context(self) -> str:
        entities = ", ".join([f"{k}: {v}" for k, v in self.memory["entities"].items()])
        return f"Known entities in this series: {entities}"

    def _save(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)
