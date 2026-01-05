import json
import requests
from bs4 import BeautifulSoup
from season_extract import extract_json_data, Player
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
    match_day = schedule.select_one('.match-days')
    day = match_day.select('.match-day')
    
    extracted_data = []
    var_test = {"date_played"}
    for each in day:
        game_played_time = []
        team = []
        result = []

        #iterate through each day
        date_played = (each.select_one('.date').string)

        games = each.select('.time')
        for game in games:
          game_played_time.append((game.get('datetime')))


        teams = each.select('.team')
        test = []
        for each in teams:
            result = each.get('class')
            #result's output is a list like this: ["red", "team", "lose"]

            teams_info = {"name": each.select('.name')[-1].string,
                          "side": result[0],
                          "result": result[-1]}
            test.append(teams_info)

        game = {}

        game["started_at"] = game_played_time
        game["teams"] = [test[0], test[1]]
        
        
        # bingo_data = {
        #     "date_played":date_played,#1
        #     "game_played_time": game_played_time,#2
        #     "teams":team,#4
        #     "result":result#4 lists of 3 items
        # }


        # bingo_data_test = {
        #     "play_date": date_played,
        #     "games":[
        #         {
        #             "started": game_played_time[0],
        #             "teams":[
        #                 {"name": , "side": , "result":},
        #                 {"name":, "side":, "result":}
        #             ]   
        #         },
        #         {
        #             "started": game_played_time[1],
        #             "teams":[
        #                 {"name": , "side": , "result":},
        #                 {"name":, "side":, "result":}
        #             ]   
        #         }
        #     ]
        # }

        # extracted_data.append(bingo_data)
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

        schedule = soup.select_one('.schedule')
        
        res = extract_match(soup)
        save_to_json("Season_5/match", res)

