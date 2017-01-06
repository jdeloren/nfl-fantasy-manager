#!/usr/bin/python

import requests
import re
from bs4 import BeautifulSoup


ROOT_URL = "http://www.pro-football-reference.com/"
TEAM_URL = "teams/"

NFL_TEAM_ARRAY = [
    'crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cle', 'dal', 'den', 'det',
    'gnb', 'htx', 'cit', 'jax', 'kan', 'ram', 'mia', 'min',
    'nwe', 'nor', 'nyg', 'nyr', 'rai', 'phi', 'pit',
    'sdg', 'sfo', 'sea', 'tam', 'oti', 'was']

def get_data(url):
    session = requests.session()
    request = session.get(url, timeout=10)

    return BeautifulSoup(request.content)

def get_data_from_root(folder):
    return get_data(ROOT_URL + folder)

def get_roster_data_for_year(franchise):
    return get_data_from_root(franchise + "/2016_roster.htm")

def get_teams_static():
    for team in NFL_TEAM_ARRAY:
        roster = get_roster_data_for_year(TEAM_URL + team)
        #print roster.find_all("td")
        players = roster.find_all("td", {"data-stat" : "player"})


        for player in players:
            print "PLAYER: "
            print player

def get_teams():
    team_doc = get_data(ROOT_URL + TEAM_URL)

    body = team_doc.find("tbody").find_all_next("a")
    print body



get_teams_static()