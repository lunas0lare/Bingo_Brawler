import json
import requests
from bs4 import BeautifulSoup
from season_extract import extract_json_data
from fileHandler import *
import time
from datetime import datetime
FILEPATH = 'config/season.json'

def html_parser(link) -> str:
    request = requests.get(link).text
    
    return request

def content_to_file(dir_name, data, file_name):
    """
    create folder and file for the data, and save the JSON into them
    """
    create_project_dir(dir_name)
    write_file(dir_name + '/' + file_name, data)

def extract_player(soup)->list:
    """
    return the information of player in form of list of Players.\n
    players: a string from soup's select\n
    type: string to defind solo or team play\n
    """

    extracted_data = []

    participate = soup.select_one('section:is(.teams, .people)')
    team_player = participate.select('.team')
    player = participate.select('div.players.runners .player')
    
    if(team_player):
        for each in team_player:
            players = each.select('.player')
            team = each.select('.name')[-1].get_text(strip = True)

            for i, player in enumerate(players):  
                extracted_data.append(
                    {
                    "name": each.select('.name span')[i].get_text(strip = True),
                    "link": player.get('href'),
                    "team": team
                }
            )
    elif (player):
        for each in player:
            extracted_data.append(
                {
                    "name": each.select_one(('.name')).get_text(strip = True),
                    "link": each.select_one('a').get('href'),
                    "team": "none"
                }
            )
    return extracted_data
    
        
def extract_match(soup)->list:
    """
    extract match from html as soup object.

    input: a soup object as html data.

    return: a list of dictionary contain the data needed.
    
    """
    schedule = soup.select_one('.schedule')
    match_day = schedule.select_one('.match-days, .schedule-container')
    day = match_day.select('.match-day, .played')
    
    extracted_data = []
    for each in day: 
        result = []

        #iterate through each day
        date_played = (each.select_one('.date').string)

        bingo_day = {
            "date_played": date_played,
            "games": []
        }

        games = each.select('.time')
        matches = each.select('.team')
        
        game_times = [g.get('datetime') for g in games]

        objs = []
        if(matches):
            for m in matches:
                result = m.get('class') or []
            #result's output is a list like this: ["red", "team", "lose"]
                objs.append({"name": m.select('.name')[-1].string,
                                "side": result[0] if len(result) > 0 else None,
                                "result": result[-1] if len(result) > 0 else None})
        
        players = each.select('[class^=player]')
        if(players):
          for red, blue in zip(players[0], players[1]):
                result_red = players[0].get('class')
                objs.append({"name": red,
                                "side": "red"})
                if(len(result_red) != 1):
                    objs[-1]["result"] = "winner"
                else:
                    objs[-1]["result"] = "loser"

                result_blue = players[1].get('class')
                objs.append({"name": blue,
                                  "side": "blue"})
                if(len(result_blue) != 1):
                    objs[-1]["result"] = "winner"
                else:
                    objs[-1]["result"] = "loser"
                  

        team_per_game = 2

        for i in range(len(game_times)):
            
            start = i * team_per_game
            end = start + team_per_game
            bingo_day["games"].append({
                "started": game_times[i],
                "teams": objs[start:end],
            })

        extracted_data.append(bingo_day)
    return extracted_data

def extract_leaderboard(soup)->list:
    
    leaderboard_raw = soup.select_one('.box.leaderboard')
    
    #column headers
    leaderboard_data = leaderboard_raw.select('tr')
    headers = leaderboard_data[0].get_text().strip().split('\n')
    extracted_data = []
    
    for each in leaderboard_data[1:len(leaderboard_data) - 1]:
        values = each.get_text().strip().split('\n')
        row_dict = dict(zip(headers, values))
        extracted_data.append(row_dict)
    return extracted_data

if __name__ == "__main__":

    # data = extract_json_data(FILEPATH)
    # seasons = data.load_season()

    # for i in range(len(seasons)):
    #     data = html_parser(seasons[i]['base_url'])
    #     content_to_file(seasons[i]['name'], data, 'content.txt')

            
        # season = input("select which season to scrape from(1-5): ")

        data = read_file(f'Season_5/content.txt')
        soup = BeautifulSoup(data, 'html.parser')
        res = extract_leaderboard(soup)
        save_to_json("Season_5/leaderboard", res)
