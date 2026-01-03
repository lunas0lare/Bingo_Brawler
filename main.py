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

def get_player_info(players, type: str)->list[Player]:
    """
    return the information of player in form of list of Players.\n
    players: a string from soup's select\n
    type: string to defind solo or team play\n
    """
    player_list = list()
    if(type == "team"):
        for each in players:
            number_player = len(each.select('.player'))
            team = each.select('.name')[-1].get_text(strip = True)
            for i in range(number_player):
                link = each.select('.player')[i].get('href')
                name = each.select('.name span')[i].get_text(strip = True)
                test_player = Player(name, link, team)
                player_list.append(test_player)
    elif (type == "solo"):
        for each in player:
            name = each.select_one('.name').get_text(strip = True)
            link = each.select_one('a').get('href')
            test_player = Player(name, link, "none")
            player_list.append(test_player)
    return player_list

def extract_match(soup):
    """
    extract match from html\n
    
    """
    schedule = soup.select_one('.schedule')
    match_day = schedule.select_one('.match-days')
    day = match_day.select('.match-day')
    
    extracted_data = []
    for each in day:
        game_played_time = []
        #iterate through each day
        date_played = (each.select_one('.date').string)

        games = each.select('.time')
        for game in games:
          game_played_time.append((game.get('datetime')))

        teams = each.select('.team')
        var = []
        result = []

        for team in teams:
            var.append(team.select('.name')[-1].string)
            result.append(team.get('class'))
           
        bingo_data = {
            "date_played":date_played,
            "game_played_time": game_played_time,
            "teams":var,
            "result":result
        }
        extracted_data.append(bingo_data)
    return extracted_data

if __name__ == "__main__":

    # data = extract_json_data(FILEPATH)
    # seasons = data.load_season()

    # for i in range(len(seasons)):
    #     data = html_parser(seasons[i]['base_url'])
    #     content_to_file(seasons[i]['name'], data, 'content.txt')
    try:
            
        # season = input("select which season to scrape from(1-5): ")

        data = read_file(f'Season_5/content.txt')
        soup = BeautifulSoup(data, 'html.parser')

        schedule = soup.select_one('.schedule')
        
        res = extract_match(soup)

        print(res[0])

        # match_day = schedule.select_one('.match-days')
        # match = match_day.select('.match-day')
        
        # date_play = match[0].select_one('.date').string

        # games = match[0].select('.time')

        # game_1 = games[0].get('datetime')
        # game_2 = games[1].get('datetime')
        # teams = match[0].select('.team')

        # print(teams[1].select('.name')[-1].string)
        #  print(teams[0].get('class')[-1])
        # print(teams[1].get('class'))

        # #extracting players/teams in html
        # participate = soup.select_one('section:is(.teams, .people)')
        
        #extracting each team/player/commentators

        # team_player = participate.select('.team')
        # player = participate.select('div.players.runners .player')
        # commentator = participate.select('.players.commentators')

        # user_data = list()
        # if(len(team_player) != 0):
        #     user_data = get_player_info(team_player, 'team')
        # elif(len(player) != 0):
        #     user_data = get_player_info(player, 'solo')
        # save_to_json(f"Season_{season}/user_data", user_data)
    except Exception as e:

        print(f"error: {e}")