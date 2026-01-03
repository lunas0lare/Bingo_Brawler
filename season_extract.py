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

@dataclass
class Player:
    name: str
    platform: str
    team: str
    
    def __init__(self):
        self.name = ""
        self.platform = ""
        self.team = "solo"
        self.role = ""
    def __init__(self, name: str = "", platform: str = "", team: str = "solo", role: str = "player"):
        self.name = name
        self.platform = platform
        self.team = team
        self.role = role
    def __str__(self):
        return f"name: {self.name}, platform: {self.platform}, team: {self.team}, role: {self.role}"
    