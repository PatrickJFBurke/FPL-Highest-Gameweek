import json
from unittest.mock import patch
import pytest
from FPL_highest_gw_score import fetch
from FPL_highest_gw_score import fetch_league_teams
from FPL_highest_gw_score import fetch_highest_gw_scores
from FPL_highest_gw_score import scores_convert

# local jsons to be returned with patched fetch
def fake_league_data():
    with open("testing/fake_league.json") as f:
        return json.load(f)
        
def fake_score_data(x):
    with open(f"testing/fake_score_data/fake_score_data_{x}.json") as f:
        return json.load(f)
    
def fake_team_data(x):
    with open(f"testing/fake_team_data/fake_team_data_{x}.json") as f:
        return json.load(f)

def fake_broken_league_data():
    with open("testing/fake_broken_league.json") as f:
        return json.load(f)
        
def fake_broken_score_data():
    with open(f"testing/fake_broken_score_data/fake_broken_score_data_1.json") as f:
        return json.load(f)
    
def fake_broken_team_data():
    with open(f"testing/fake_broken_team_data/fake_broken_team_data_1.json") as f:
        return json.load(f)

# check program exits if invalid response from server
def test_fetch():
    with pytest.raises(SystemExit):
        fetch("xxxxxxxxxx")

# patch fetch to return local json data for testing
@patch("FPL_highest_gw_score.fetch")
def test_fetch_league_teams(mock_fetch):
    
    # patch input to bypass while loop
    with patch("builtins.input", return_value="1"):

        # check function correctly returns team ids
        mock_fetch.return_value = fake_league_data()
        assert fetch_league_teams() == [1, 2, 3, 4, 5, 6, 7, 8]

        # check function correctly exits if expected json data is not returned
        mock_fetch.return_value = fake_broken_league_data()
        with pytest.raises(SystemExit):
            fetch_league_teams()


    # patch input to check exit works correctly
    with patch("builtins.input", return_value="0"):
            with pytest.raises(SystemExit):
                fetch_league_teams()

 
highest = {
    1:[4,94],
    2:[4,89],
    3:[1,78],
    4:[1,84],
    5:[1,74],
    6:[4,83],
    7:[4,81],
    8:[4,78]
    }


# patch fetch to return local json data for testing
@patch("FPL_highest_gw_score.fetch")
def test_fetch_highest_gw_scores(mock_fetch):
    # check highest scores matches expected from local json data
    side_effect = []
    for i in range(1,9):
        side_effect.append(fake_score_data(i))
    mock_fetch.side_effect = side_effect

    assert fetch_highest_gw_scores([1, 2, 3, 4, 5, 6, 7, 8]) == highest

    # check unexpected json format exits correctly
    mock_fetch.side_effect = None
    mock_fetch.return_value = fake_broken_score_data()
    with pytest.raises(SystemExit):
        fetch_highest_gw_scores([1])


# patch fetch to return local json data for testing
@patch("FPL_highest_gw_score.fetch")
def test_scores_convert(mock_fetch):
    # check score conversion matches expected from local json data
    side_effect = []
    for i in range(1,9):
        side_effect.append(fake_team_data(i))
    mock_fetch.side_effect = side_effect

    scores = {
        "Anthony Anderson":[4,94],
        "Bob Billing":[4,89],
        "Charlie Crumb":[1,78],
        "David Daniels":[1,84],
        "Edward Ederson":[1,74],
        "Frank Farrier":[4,83],
        "Gordon Godwick":[4,81],
        "Harry Hendricks":[4,78]
        }

    assert scores_convert(highest) == scores

    # check unexpected json format exits correctly
    mock_fetch.side_effect = None
    mock_fetch.return_value = fake_broken_team_data()
    with pytest.raises(SystemExit):
        scores_convert(highest)
