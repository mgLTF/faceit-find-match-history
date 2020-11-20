import json
import requests
import math
import sys
from requests.auth import HTTPBasicAuth
from pprint import pprint

URL = "https://open.faceit.com/data/v4/"
API_KEY = "ec7bd30e-26b9-484d-ae61-0fdbe159668a"
headers = {'Authorization': 'Bearer ' + API_KEY}

#TODO: flag para checkar pelo jogador q quiser
#TODO: flag para mudar o n de jogos

# returns playerID from playerNickname. Returns None if player wasn't found
def get_player_id(player_nickname):
    req = requests.get("{}players?nickname={}&game=csgo".format(URL, player_nickname), headers=headers)
    if req.status_code == 200:
        id = req.json()["player_id"]
        return id

    return None

# returns amount of matches from given player
def get_number_of_matches(player_id):
    req = requests.get("{}players/{}/stats/csgo".format(URL, player_id), headers=headers)
    
    if req.status_code == 200:
        return int(req.json()["lifetime"]["Matches"])
    return None

def get_last_matches(playerID, off, n):
    req = requests.get("{}players/{}/history?game=csgo&offset={}&limit={}&from=0".format(URL, playerID, off, n), headers=headers)
    
    if req.status_code == 200:
        matches = req.json()
        return matches["items"]

        #print(len(matches["items"]))

    return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python3 main.py [player1] [player2]")
        sys.exit(1)

    
    player1 = sys.argv[1]
    player2 = sys.argv[2]
    
    player1_id = get_player_id(player1)
    player2_id = get_player_id(player2)

    # stop program if one of the players was not found
    if player1_id == None:
        print("Player {} was not found.".format(player1_id))
        sys.exit(1)
    elif player2_id == None:
        print("Player {} was not found.".format(player2_id))
        sys.exit(1)

    # get match list from player with least matches
    player1_matches = get_number_of_matches(player1_id)
    player2_matches = get_number_of_matches(player2_id)
    
    if player2_matches < player1_matches:
        temp = player1
        player1 = player2
        player2 = temp

        temp = player1_id
        player1_id = player2_id
        player2_id = temp

        temp = player1_matches
        player1_matches = player2_matches
        player2_matches = temp

    matches = []
    if player1_matches >= 500:
        cycles = 5
    else:
        cycles =  math.ceil(player1_matches / 100)   

    i = 0
    while i < cycles:
	    matches.extend(get_last_matches(player1_id, i*100, 100))
		#print((i*100)/1025)-JPC-
	    i += 1

    json.dumps(matches, indent=4)
    print("Checking for {}'s last {} matches...".format(player1, len(matches)))
    found_matches = [i["match_id"] for i in matches if player2_id in i["playing_players"]]		
    print("Found {} matches.".format(len(found_matches)))
    pprint(found_matches)

