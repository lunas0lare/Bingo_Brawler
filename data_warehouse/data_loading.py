import json 
import os
def load_data(season: int) -> dict[str, str]:
    folder = f'Season_{season}'
    datasets = dict()
    try:
       
        for filename in os.listdir(folder):
            if (filename.endswith('json')):
                path_name = os.path.join(folder, filename)
                key = os.path.splitext(filename)[0]
                with open(path_name, 'r', encoding = 'utf-8') as raw_data:
                    datasets[key] = json.load(raw_data)
        return datasets
        
    except FileNotFoundError:
        print(f"File not found: {path_name}")   
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in file {path_name}: {e}")

def load_season_list():
    dataset = dict()
    with open('config/season.json', 'r', encoding='utf-8') as raw_data:
        dataset['season'] = json.load(raw_data)
    return dataset
