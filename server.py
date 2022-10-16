from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import uvicorn
import json

app = FastAPI()

app.mount("/client", StaticFiles(directory="client"), name="client")

team_to_ids = {
    "lakers": "1610612747",
    "warriors": "1610612744",
    "heat": "1610612748",
    "suns": "1610612756"
}

players = []
dream_team = []


@app.get("/")
async def get_client():
    return FileResponse('client\index.html')


def _is_in_dream_team(id):
    global dream_team
    if len(list(filter(lambda p: p["id"] == id, dream_team))) > 0:
        return True
    return False


def _get_stats(first_name, last_name):
    stats = requests.get(
        f"https://nba-players.herokuapp.com/players-stats/{last_name.lower()}/{first_name.lower()}")
    first_five_stats = []
    if (stats.text != 'Sorry, that player was not found. Please check the spelling.'):
        res = json.loads(stats.text)
        counter = 0
        for key, value in res.items():
            if counter > 4:
                break
            first_five_stats.append(f"{key}: {value}".replace("_", " "))
            counter += 1
    return first_five_stats


def _get_team_players(team, players):
    global dream_team
    team_id = team_to_ids[team]
    players_list = [*players["league"]["africa"],
                    *players["league"]["sacramento"],
                    *players["league"]["standard"],
                    *players["league"]["utah"],
                    *players["league"]["vegas"]]
    return [{
            "id": p["personId"],
            "name": f"{p['firstName']} {p['lastName']}",
            "jersey_number": p["jersey"],
            "position":p["pos"],
            "picture":f"https://nba-players.herokuapp.com/players/{p['lastName'].lower()}/{p['firstName'].lower()}",
            "stats":_get_stats(p['firstName'], p['lastName']),
            "has_date_of_birth":p["dateOfBirthUTC"] != "",
            "date_of_birth":p["dateOfBirthUTC"],
            "in_dream_team": _is_in_dream_team(p["personId"])} for p in players_list if p["teamId"] == team_id]


@app.get("/myNBA/players")
async def get_players(year, team, has_birth_date=False):
    global players
    players = requests.get(
        f'http://data.nba.net/10s/prod/v1/{year}/players.json')
    players = _get_team_players(team, players.json())
    res = players
    if (has_birth_date == 'true'):
        res = list(filter(lambda p: p["has_date_of_birth"], players))
    return res.copy()


@app.get("/myNBA/dream-team")
async def get_dream_team():
    global dream_team
    return dream_team


@app.post("/myNBA/dream-team/{player_id}")
async def add_to_dream_team(player_id):
    global dream_team
    global players
    player = list(filter(lambda p: p["id"] == player_id, players))[0]
    player["in_dream_team"] = True
    dream_team.append(player)
    return players


@app.delete("/myNBA/dream-team/{player_id}")
async def remove_from_dream_team(player_id):
    global players
    global dream_team
    player = list(filter(lambda p: p["id"] == player_id, players))
    if (len(player) > 0):
        player[0]["in_dream_team"] = False
    dream_team = list(filter(lambda p: p["id"] != player_id, dream_team))
    return dream_team


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
