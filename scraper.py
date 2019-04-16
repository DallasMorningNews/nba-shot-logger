import csv
import json
import requests
import sys
import time

# placeholder list that will hold all the shot data for Dirk's career
player_shots = []


################################################################################
# GETTING THE SHOTS
# Retrieves shot and game log data from the NBA api and constructs a row for
# each shot in the shot data, using game log data to cross reference clean dates,
# teams and opponent
################################################################################

def get_shots(year, season_type, shot_id):
    # required arguments for the shot api endpoint
    payload = {
        "Period": "0",
        "VsConference": "",
        "LeagueID": "00",
        "LastNGames": "0",
        "TeamID": "0",
        "PlayerPosition": "",
        "Location": "",
        "Outcome": "",
        "ContextMeasure": "FGA",
        "DateFrom": "",
        "StartPeriod": "",
        "DateTo": "",
        "OpponentTeamID": "0",
        "ContextFilter": "",
        "RangeType": "",
        "Season": year,
        "AheadBehind": "",
        "PlayerID": player,
        "EndRange": "",
        "VsDivision": "",
        "PointDiff": "",
        "RookieYear": "",
        "GameSegment": "",
        "Month": "0",
        "ClutchTime": "",
        "StartRange": "",
        "EndPeriod": "",
        "SeasonType": season_type,
        "SeasonSegment": "",
        "GameID": ""
    }

    # required arguments for the gamelog api endpoint
    games_payload = {
        "LeagueID": "00",
        "PlayerID": player,
        "Season": year,
        "SeasonType": season_type
    }

    # defining the requests for the shots and games api
    r = requests.get("http://stats.nba.com/stats/shotchartdetail", params=payload, headers=BROWSER_HEADERS, timeout=15)
    r.raise_for_status()
    s = requests.get("http://stats.nba.com/stats/playergamelog", params=games_payload, headers=BROWSER_HEADERS, timeout=15)
    s.raise_for_status()

    # converting the response to the above calls to json
    shot_data = r.json()
    game_logs = s.json()

    # defining the shots in the shot data
    shot_sets = shot_data["resultSets"][0]["rowSet"]

    # defining the games in the games data
    games = game_logs["resultSets"][0]["rowSet"]

    # for each shot in the shots data
    for shot in shot_sets:

        # placeholder for the date, teams and opponent of each game
        shotDate = ""
        teams = ""
        opponent = ""

        # go through the games data, match up the game id across the games data and
        # the shot data, then set shotDate, teams and opponent
        for game in games:
            if game[2] == shot[1]:
                shotDate = game[3]
                teams = game[4]
                opponent = teams[-3:]


        # assign values for each column from the shot data
        game_id = shot[1]
        period = shot[7]
        minutes_remaining = shot[8]
        seconds_remaining = shot[9]
        result = shot[10]
        shot_type = shot[11]
        shot_value = shot[12]
        shot_zone = shot[13]
        shot_range = shot[15]
        shot_distance = shot[16]
        shot_xlocation = shot[17]
        shot_ylocation = shot[18]
        home_team = shot[22]
        away_team = shot[23]

        # append the shot to the dirk list
        player_shots.append([shot_id, year, season_type, game_id, shotDate, teams, period, minutes_remaining, seconds_remaining, result, shot_type, shot_value, shot_zone, shot_range, shot_distance, shot_xlocation, shot_ylocation, opponent, home_team, away_team])

        #increment the shot id
        shot_id += 1

    # pause after each season
    time.sleep(5)

    #return the shot_id value to continue incrementing it across years and season types
    return shot_id


################################################################################
# RUNNING THE DATA RETRIEVAL
# Given a list of years, perform the get_shots function, supplying the year, season_type
# and current shot_id (used for uniquely id-ing each shot)
################################################################################

def scrape(years):

    # start with an id of 0
    shot_id = 0

    # for each year in the years list
    for year in years:
        # alert the user to the current year data is being retrieved for
        print("Getting shots for {0}".format(year))

        # for each season_type, get the shots corresponding to that year and season
        for type in season_type:
            shot_id = get_shots(year, type, shot_id)


    # once all shots have been retrieved for the given years, dump the data into
    # a file as a csv
    with open(output_file, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(["ID","SEASON","SEASON TYPE","GAME ID","DATE","TEAMS","QUARTER","MINUTES REMAINING","SECONDS REMAINING","RESULT","SHOT TYPE","SHOT VALUE","SHOT AREA","SHOT RANGE","SHOT DISTANCE","SHOT X LOCATION","SHOT Y LOCATION","OPPONENT","HOME TEAM","AWAY TEAM"])
        writer.writerows(player_shots)

    writeFile.close()


################################################################################
# INITIAL SETUP
# Formats the arguments passed in via the command line and prepares them for use
# in the data retrieval process
################################################################################

# list of arguments passed from command line
args = sys.argv

# converts the player id to a string
player = str(args[1])

#converts the start and end years to integers
start_year = int(args[2])
end_year = int(args[3])


# perfroms some sanity checks on the arguments supplied. Checks that the start_year
# preceeds the end_year, that the required minimum amount of arguments is present,
# and that an accepted value is passed for the season_type argument

if start_year >= end_year:
    print("Please supply a valid start year and end year")
elif len(args) < 3:
    print("Please supply all of the required arguments. See documentation for help.")
elif str(args[4]) != "Regular_Season" and str(args[4]) != "Playoffs" and str(args[4]) != "All":
    print("Please supply a valid season type. Valid response are Regular_Season, Playoffs or All")
else:

    # if all conditions are met, parse the season_type argument into the correct format
    # expected by the NBA api
    if len(args) == 3:
        season_type = ['Regular Season']
    elif str(args[4]) == 'All':
        season_type = ['Regular Season', 'Playoffs']
    else:
        season_type = [str(args[4]).replace('_', ' ')]

    # set a placeholder list for our years
    years = []

    # populate that list with all of the season sets between the start year and
    # end year in the correct format (ex: 1998-99)
    for x in range(start_year, end_year):
        season = str(start_year) + '-' + str((start_year + 1))[-2:]
        years.append(season)

    # set the output_file name based on the supplied arguments
    output_file = "data-output/player-{0}_years-{1}-{2}_shots.csv".format(player, start_year, end_year)

    # headers info for requesting from the nba api
    BROWSER_HEADERS = {
        'user-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'), # noqa: E501
        'Dnt': ('1'),
        'Accept-Encoding': ('gzip, deflate, sdch'),
        'Accept-Language': ('en'),
        'origin': ('http://stats.nba.com')
    }

    scrape(years)
