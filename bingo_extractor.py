import traceback
from bs4 import BeautifulSoup
from season_extract import extract_json_data
from fileHandler import *
FILEPATH = 'config/season.json'

def extract_players(soup)->list:
    """
    Extracts player information from an HTML document into a structured format.

    The function supports 2 page structures:
    1. Team-based pages where players are grouped under teams.
    2. Individual-based pages where players are listed without teams.

    Args:
        soup (BeautifulSoup): Parse HTML document of the website.

    Returns:
        list[dict]: A list of player records. Each record contains:
        - name (str): Player name
        - link (str): URL to the players page
        - team (str): Team name, or "none" if not applicable
    """

    extracted_data = []

    participate = soup.select_one('section:is(.teams, .people)')
    team_player = participate.select('.team')
    player = participate.select('div.players.runners .player')
    
    #case 1: team-based player layout
    if(team_player):
        for each in team_player:
            players = each.select('.player')
            team = each.select('.name')[-1].get_text(strip = True) #last index is the team's name

            for i, player in enumerate(players):  
                extracted_data.append(
                    {
                    "name": each.select('.name span')[i].get_text(strip = True),
                    "link": player.get('href'),
                    "team": team
                }
            )
    #case 2: individual player layout (no teams)
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
    Extracts match schedule data from an HTML document into a structured format.

    The function looks for a schedule section and iterates through each match day. 
    For each day, it collects the date, game start times, and the two teams/players
    participating per game. It normalizes output into a list of "day" objects, where 
    each day contains a list of games. 

    Expected output schema:
        [
            {
                "date_played": str,
                "games": [
                    {
                        "started": str | None,   # e.g., ISO datetime string from <time datetime="...">
                        "teams": [
                            {
                                "name": str | None,
                                "side": str | None,     # "red" / "blue" (or parsed from CSS class)
                                "result": str | None    # "winner" / "loser" (or parsed from CSS class)
                            },
                            ...
                        ]
                    },
                    ...
                ]
            },
            ...
        ]

    Args:
        soup (BeautifulSoup): Parse HTML document of the website.

    Returns:
        list[dict]: A list of match-day objects, each containing date and games.
    
    Notes:
    - This function assumes each game has exactly 2 participants(team_per_game = 2)
    - It relies on specific CSS selectors (".schedule", ".match-day", ".time", ".teams",
    and classes that start with "player").
    - If the HTML strucutre changes or expected elements are missing, this function raise attribute error 
    (e.g., if ".schedule" is not found)

    """
    extracted_data = []

    schedule = soup.select_one('.schedule')
    match_day = schedule.select_one('.match-days, .schedule-container')
    day_blocks = match_day.select('.match-day, .played')

    #iterate through each day block(one date containing multiple games)
    for each in day_blocks: 
        # bingo_day = {
        # }

        participants = []

        #case 1: Team-based layout(teams have CSS classes like "red", "lose"...)
        team_elements = each.select('.team')
        if(team_elements):
            for t in team_elements:
                team_classes = t.get('class') or [] #e.g. ["red", "team", "lose"]
                participants.append({"name": t.select('.name')[-1].string,
                                "side": team_classes[0] if team_classes else None,
                                "result": team_classes[-1] if team_classes else None})
        
        #case 2: player-based layout(2 groups: red and blue players)

        player_elemments = each.select('[class^=player]')
       
        if(player_elemments):
           for red_side, blue_side in zip(player_elemments[0], player_elemments[1]):
                result_red = player_elemments[0].get('class')
                participants.append(
                    {"name": red_side,
                    "side": "red",
                    "result": "winner" if len(result_red) != 1 else "loser"}
                    )
               
                result_blue = player_elemments[1].get('class')
                participants.append(
                    {"name": blue_side,
                    "side": "blue",
                    "result": "winner" if len(result_blue) != 1 else "loser"})

        #Assumption: each game has exactly 2 participants (red vs blue)
        team_per_game = 2

        #extract game start timestamps(one per game)
        time_elements = each.select('.time')
        game_start_times = [t.get('datetime') for t in time_elements]

        #pairing each start time with the next 2 participants.
        for i in range(len(game_start_times)):
            start = i * team_per_game
            end = start + team_per_game
            extracted_data.append({
                "started": game_start_times[i],
                "teams": participants[start:end],
            })

        # extracted_data.append(bingo_day)
    return extracted_data

def extract_leaderboard(soup)->list:
    """
    Extracts leaderboard table data from an HTML document.

    The function locates the leaderboard table, reads the first row as column
    headers, and maps each subsequent row into a dictionary keyed be those headers.
    Args:
        soup (BeautifulSoup): a Parsed HTMl document of the website.

    Returns:
        list[dict]: A list of leaderboard rows. Each row is represented as a dicitonary where keys
        are column headers and values are the corresponding cell values.
    
    Notes:
    - Assumes the first <tr> contains column headers.
    - skips the final row(typically a footer or summary row).
    - Relies on newline-separated text within table rows.
    """
    extracted_data = []

    leaderboard_raw = soup.select_one('.box.leaderboard')
    leaderboard_data = leaderboard_raw.select('tr')

   
    #leaderboard header
    headers = leaderboard_data[0].get_text().strip().split('\n')
    headers.insert(0, "index")
    #subsequent leaderboard row. 
    for each in leaderboard_data[1:len(leaderboard_data) - 1]:
        values = each.get_text().strip().split('\n')
        row_dict = dict(zip(headers, values))

        #remove the last data row, which is the description
        if(len(values[0]) < 10):
            extracted_data.append(row_dict)
    return extracted_data

def extract_playoff(soup) -> list:
    """
    Extracts playoff bracket match data from an HTML document.

    The function parses a playoff bracket structure, extracting match dates played and team information(team rows)
    for each matchup in match tables. Each match is normalized into a dictionary containing the match date and a list of 
    participating teams.

    Expected output schema:
        [
            {
                "date_played": str,   # ISO datetime string
                "teams": [
                    {
                        <header_field>: <value>,
                        ...,
                        "side": "red" | "blue"
                    },
                    ...
                ]
            },
            ...
        ]
    Args:
        soup (BeautifulSoup): Parsed HTML document of a website.

    Returns:
        list[dict]: A list of playoff match objects, each containing the match date and associated team data.
    
    Notes:
    - Assumes the first playoff match contains table headers(<thead>).
    - Team rows are parsed from <tbody>.
    - Teams are assigned sides alternately: even index = "red, odd = "blue".
    - Relies on space-separated text extraction from table rows.
    """
    extracted_data = []

    matches_raw = soup.select_one('.bracket')
    matchs_tables = matches_raw.select('[class^=match]')
    #playoff header got from first match table
    header = matchs_tables[0].thead.select_one('tr').get_text(" ", strip = True).split(' ')
    
    #parse each match table into a normalized object
    for each in matchs_tables: 
        playoff_data = {
        "date_played": "",
        "teams": []     
            }
        date_played = each.select_one('.datetime').get('datetime')
        playoff_data['date_played'] = date_played

        team_data = []
        team_rows = each.tbody.find_all('tr')

        for i, t in enumerate(team_rows):
            row_values = t.get_text(" ", strip = True).split(' ')
            #handle multi-word teams name: if second item is not a number, 
            #it mean team has 2 word name.
            if (not row_values[1].isdigit()):
                row_values = [' '.join(row_values[:2])] + row_values[2:]

            #map header -> row values to build a structured team 
            team_data = dict(zip(header, row_values))   
            team_data["side"] = "red" if i % 2 == 0 else "blue"
            
            playoff_data['teams'].append(team_data)

        extracted_data.append(playoff_data)
    return extracted_data
