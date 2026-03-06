import json
from pathlib import Path
from dataclasses import dataclass

class extract_json_data:
    """
    extract season data from json file
    """
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)

    def load_season(self) -> list[dict]:

        if(not self.config_path.exists()):
            raise FileNotFoundError(f"season config not found: {self.config_path}")

        with self.config_path.open('r', encoding='utf-8') as file:
            data = json.load(file)
        
        return data