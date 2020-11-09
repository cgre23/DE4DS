import time
import random
import sqlite3
from gazpacho import get, Soup
import pandas as pd
from rich import print
from tqdm import tqdm


def nfl_week(date=None):
    if not date:
        date = pd.Timestamp("now")
    day_of_year = pd.Timestamp(date).dayofyear
    start_day = pd.Timestamp("2020-09-08").dayofyear
    week = (day_of_year - start_day) // 7
    return week


def parse_tr(tr):
    last, first = tr.find("td", {"class": "playerLink"}).find('a').text.split(", ")
    data = tr.find("td", {"nowrap": ""})
    position = data[3].find("font").text
    yards_pass = float(data[4].text.replace("*", ""))
    yards_rush = float(data[6].text.replace("*", ""))
    yards_receiving = float(data[9].text.replace("*", ""))
    return {
        "name": f"{first} {last}",
        "position": position,
        "yards": yards_pass + yards_rush + yards_receiving
    }


def parse_all_trs(trs):
    players = []
    for tr in trs:
        try:
            player = parse_tr(tr)
            if player['position'] in ["QB", "WR", "RB", "TE"]:
                players.append(player)
        except AttributeError:
            pass
    return players


def scrape_data_for(*, date=None, week=None):
    if (date and week) or (not date and not week):
        raise Exception("Choose one of date= or week=")
    if date:
        week = nfl_week(date)
    url = "https://www.fantasysharks.com/apps/bert/stats/points.php"
    segment = week + 691
    params = {"League": -1, "Position": 99, "scoring": 13, "Segment": segment}
    soup = Soup.get(url, params)
    trs = soup.find("table", {"id": "toolData"}).find("tr")
    data = parse_all_trs(trs)
    df = pd.DataFrame(data)
    df['week'] = week
    df['fetched_at'] = pd.Timestamp("now")
    return df


if __name__ == "__main__":
    con = sqlite3.connect("data/football.db")

    df = pd.DataFrame()
    for week in tqdm(range(1, 8+1)):
        idf = scrape_data_for(week=week)
        df = df.append(idf)
        time.sleep(random.uniform(1, 10)/10)
    df = df.reset_index(drop=True)

    df.to_csv("data/football.csv", index=False)
    df.to_sql(name="yards", con=con, if_exists="replace", index=False)
