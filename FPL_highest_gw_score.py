import requests
import sys
import pandas as pd

# base url for interacting with the FPL API
base_url = "https://fantasy.premierleague.com/api/"

def main():
    # get league id and teams
    teams = fetch_league_teams()

    # fetch managers gameweek history and get highest scoring week
    scores = fetch_highest_gw_scores(teams)

    # fetch player names and replace team ids with them
    scores_conv = scores_convert(scores)

    # present sorted table of high scores
    highest_scoring(scores_conv)

# API call function
def fetch(url):
    response = requests.get(base_url + url)
    if response.status_code == 200:
        return response.json()
    
    else:
        print("Cannot connect to server")
        sys.exit(0)

# fetch front page of league (50 teams) team entry numbers for use in highest scoring GW
def fetch_league_teams() -> list:
    while True:
        league_id = input("Enter League ID (Enter 0 to exit): ")

        try:
            league_id = int(league_id)

            if league_id == 0:
                print("Exiting program...")
                sys.exit(0)

            if league_id < 0:
                raise ValueError
            
            r = fetch(f"leagues-classic/{league_id}/standings/")

            if "detail" in r: # detail is only present when using a valid league id that does not have an associated league
                raise ValueError
            
            else:
                break

        except ValueError:
            print("Invalid League ID")
    
    team_entries = []
    try:
        for team in r["standings"]["results"]:
            team_entries.append(team["entry"])

    except KeyError: # catches if the api call does not return the expected format
        print("FPL API has changed, contact developer")
        sys.exit(0)

    return team_entries

# no checks required as a valid league will always return valid team IDs
def fetch_highest_gw_scores(team_ids: list) -> dict:

    highest_scores = {}

    for team in team_ids:
        r = fetch(f"entry/{team}/history/")

        highest = 0
        try:
            for gameweek in r["current"]:
                if gameweek["points"] > highest:
                    highest = gameweek["points"]
                    week = gameweek['event']

        except KeyError: # catches if the api call does not return the expected format
            print("FPL API has changed, contact developer")
            sys.exit(0)

        highest_scores[team] = [week, highest]       

    return highest_scores


# convert team id into player names
def scores_convert(scores: dict) -> dict:
    
    scores_conv = {}

    try:
        for team in scores:
            r = fetch(f"entry/{team}/")
            scores_conv[r["player_first_name"] + " " + r["player_last_name"]] = scores[team]

    except KeyError: # catches if the api call does not return the expected format
        print("FPL API has changed, contact developer")
        sys.exit(0)

    return scores_conv


# put the scoring data in a dataframe for presentation
def highest_scoring(scores_conv: dict):

    df = pd.DataFrame(scores_conv, index=["Gameweek", "Score"])
    df = df.transpose().sort_values(["Score"], ascending=False)

    print(df)

if __name__ == "__main__":
    main()