import traceback
from bs4 import BeautifulSoup
from season_extract import extract_json_data
from fileHandler import *
from bingo_extractor import *
FILEPATH = 'config/season.json'

if __name__ == "__main__":

    data = extract_json_data(FILEPATH)
    seasons_json = data.load_season()
    season_id_list = []
    
    for season in seasons_json:
        data = html_parser(season['base_url'])
        content_to_file(season['name'], data, 'content.txt')
        season_id_list.append(season['season_id'])
    while True:
        try:
            
            season = int(input(f"select which season to scrape from(1-{season_id_list[0]}) or 0 to quit: "))

            if(season == 0):
                print("existing.")
                break
            
            if(type(season) != int):
                raise ValueError("season must be a number")
            
            if(season not in season_id_list):
                raise ValueError("not in range!")
            

            data = read_file(f'Season_{season}/content.txt')
            soup = BeautifulSoup(data, 'html.parser')

            print("crawling player data...")
            save_to_json(f"Season_{season}/player", extract_players(soup))

            print("crawling match data...")
            save_to_json(f"Season_{season}/match", extract_match(soup))

            print("crawling leaderboard data...")
            save_to_json(f"Season_{season}/leaderboard", extract_leaderboard(soup))

            print("crawling playoff data...")
            save_to_json(f"Season_{season}/playoff", extract_playoff(soup))

        except FileNotFoundError as e:      
            print(f"file not found: {e}")
            continue
        except ValueError as e:
            print(f"input error: {e}")
            continue
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            continue
                
            
   
