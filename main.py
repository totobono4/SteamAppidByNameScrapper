import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

last_appid_param = '&last_appid={}'
max_results_param = '&max_results={}'
key_param = '?key={}'
steam_request = 'https://api.steampowered.com/IStoreService/GetAppList/v1/{}{}{}'
steam_key = os.environ.get('STEAM_KEY')
max_results = 50000

x = requests.get(steam_request.format(key_param.format(steam_key), max_results_param.format(max_results), ''))

games = []

while x.json()['response'] != {}:
    last_appid = 0

    for app in x.json()['response']['apps']:
        game = {
            'appid': app['appid'],
            'name': app['name']
        }
        games.append(game)
        last_appid = app['appid']

    x = requests.get(steam_request.format(key_param.format(steam_key), max_results_param.format(max_results), last_appid_param.format(last_appid)))

steam_games = {'games': games}

with open('steam_games.json', 'w', encoding='utf-8') as f:
    json.dump(steam_games, f, ensure_ascii=False)

print(f'Saved {len(games)} games to steam_games.json')
