### What this is

This is a python script that, given an NBA player ID, a range of years, and optionally, a season type, will return all shots by that player within that range as a csv.

### Setup

None. Just clone the repo and you're good to go.

### How to use

From the project's root directory, run `python scraper.py <player_id> <start_year> <end_year> <season_type>`

- **playerid**: Each NBA player has a unique id that identifies them within the NBA stats api. The easiest way to find a given ID is by searching for that player on the [NBA Stats page](https://www.nba.com/stats), then pulling the number from the end of the resulting URL.
- **start_year:** The first year you wish to retrieve shots for. Format is YYYY (Ex: 1999)
- **end_year:** The last year you wish to retrieve stats for. Format is YYYY (Ex: 2010). NBA seasons span two years. The `end_year` is the second year in an NBA season.
- **season_type:** `Regular_Season`, `Playoffs`, or `All`, if you want both regular season and playoff shots over a given range. If not season type is specified, only regular season shots will be retrieved. 

Example, to get Dirk Nowitzki's shots from 2000 to 2010 for both the regular season and playoffs, one would run:
`python scraper.py 1717 2000 2010 All`

### Where does the output go?

CSV files are outputted as `player-<player_id>_years-<start_year>-<end_year>_shots.csv` into the `data-output` folder within the cloned repo.

### What does the data include?

Each row in the csv represents one shot, and includes:
- **ID:** A unique identifer for the shot
- **SEASON:** The year in which the shot occurred
- **SEASON TYPE:** Regular season or playoffs
- **GAME ID:** The game id number supplied by the NBA
- **DATE:** The date on which the game occurred
- **TEAMS:** The teams involved
- **QUARTER:** Which quarter the shot occurred in
- **MINUTES REMAINING:** How many minutes were remaining in the quarter
- **SECONDS REMAINING:** How many seconds were remaining in the quarter
- **RESULT:** Whether the shot was made or missed
- **SHOT TYPE:** The type of shot (jump shot, dunk, fadeaway, etc)
- **SHOT VALUE:** 2-point field goal or 3-point field goal
- **SHOT AREA:** The area in which the shot occurred (mid range, restricted area, above the break 3, etc)
- **SHOT RANGE:** Range in feet of the shot (Less than 8 feet, 24+ ft, etc)
- **SHOT DISTANCE:** The distance of the shot in feet
- **SHOT X LOCATION:** The x location on the court of the shot (more on this below)
- **SHOT Y LOCATION:** The y location on the court of the shot (more on this below)
- **OPPONENT:** Who the opposing team was
- **HOME TEAM:** Who the home team was
- **AWAY TEAM:** Who the away team was

### What if I want to make a shot chart visualization

Perfect. A shot's `x location` can range from 250 to -250, while its `y location` can range from -50 to 890, with the player's basket resting at 0, 0. The `x` and `y` values correspond to feet on the court. For example, an `x location` of 50 is 5 feet to the right side of the basket. A `y location` of 184 is 18.4 feet down the court from the basket. Negative `y locations` are in the are between the basket and the baseline. 

You can use these `x and y locations` to plot shots in D3, QGIS, or even mapping software like Mapbox.
