#!/usr/bin/python

import urllib2
import time

import json

import requests
from bs4 import BeautifulSoup, Comment, NavigableString


ROOT_URL = "http://www.pro-football-reference.com/"
TEAM_URL = "teams/"

NFL_TEAM_ARRAY = [
    'crd', 'atl', 'rav', 'buf', 'car', 'chi', 'cle', 'dal', 'den', 'det',
    'gnb', 'htx', 'cit', 'jax', 'kan', 'ram', 'mia', 'min',
    'nwe', 'nor', 'nyg', 'nyr', 'rai', 'phi', 'pit',
    'sdg', 'sfo', 'sea', 'tam', 'oti', 'was']


def get_url_data_with_wait(url):
    data = urllib2.urlopen(url)
    time.sleep(5)
    return data.read()

def get_url_data(url):
    session = requests.session()
    request = session.get(url, timeout=10)
    return request.content

def get_data(url):
    print "URL: " + url

    return BeautifulSoup(get_url_data(url))

def get_data_from_root(folder):
    return get_data(ROOT_URL + folder)

def get_roster_data_for_year(franchise):
    return get_data_from_root(franchise + "/2016_roster.htm")



def parse_embedded_singular_data(parent, element, index):
    for child in parent[index].children:
        text = str(child.string.encode('utf-8')).strip()
        if (len(text) > 0):
            return text

    return "NONE"

def get_player_data(player_url):
    return get_data(ROOT_URL + player_url)

def parse_player_data(url):
    player = get_player_data(url)

    data = {}

    head = player.find_all('p')

    data['Name'] = parse_embedded_singular_data(head, 'p', 0)
    data['Position'] = parse_embedded_singular_data(head, 'p', 1)


    print json.dumps(data)


def get_teams_static():
    for team in NFL_TEAM_ARRAY:
        roster = get_roster_data_for_year(TEAM_URL + team)

        #players = roster.find_all("td", {"data-stat" : "uniform_number"})
        #for player in players:
        #    print "PLAYER: "
        #    print player


        for comment in roster.findAll(text=lambda text:isinstance(text, Comment)):
            for word in comment.split('\n'):
                if "uniform_number" in word and "csk" in word:
                    #print "HI: " + word
                    #print BeautifulSoup(word).find("a")['href']
                    player = parse_player_data(BeautifulSoup(word).find("a")['href'])
                    return

        return

def get_teams():
    team_doc = get_data(ROOT_URL + TEAM_URL)

    body = team_doc.find("tbody").find_all_next("a")
    print body



get_teams_static()