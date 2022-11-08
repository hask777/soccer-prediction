import requests


standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

data = requests.get(standings_url)

# print(data.text)

from bs4 import BeautifulSoup
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]
# print(standings_table)
links = standings_table.find_all('a')
# print(links)
links = [l.get("href") for l in links]
# for l in links:
#     print(l)
links = [l for l in links if '/squads/' in l]
team_urls = [f"https://fbref.com{l}" for l in links]
team_url = team_urls[0]
data = requests.get(team_url)
# print(team_urls)


import pandas as pd

matches = pd.read_html(data.text, match="Scores & Fixtures")
# print(matches[0])

soup = BeautifulSoup(data.text)
links = soup.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if l and 'all_comps/shooting/' in l]
data = requests.get(f"https://fbref.com{links[0]}")

shooting = pd.read_html(data.text, match="Shooting")[0]
shooting.columns = shooting.columns.droplevel()

# print(shooting["Date"])

# print(shooting)

team_data = matches[0].merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
# print(team_data.head())
# print(shooting.shape)

import loop

