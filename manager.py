from map import map_load, map_get, map_set, spawn_ores
from random import randint

current_section="caving"

current_map={
    "width": 0,
    "height":0,
    "data":[],
    "ladder_spots": 0
}

player={
    "x":0,
    "y":0,
    "health": 10,
    "max_health": 10,
    "name": "PlayerName",
    "inventory": {}
}

def set_map_programatically(map_type):
    global current_map
    global player

    map=""
    if (map_type=="new_cave"):
        map=f"caves/{randint(0,2)}"
    current_map,player["x"],player["y"]=map_load(f"maps/{map}")

def set_map(map):
    global current_map
    global player

    current_map,player["x"],player["y"]=map_load(f"maps/{map}")

def gen_map():
    global current_map
    global player

    spawn_ores(current_map,player["x"],player["y"])


def mget(x,y):
    return map_get(x,y,current_map)

def mset(x,y,v):
    map_set(x,y,v,current_map)

def set_section(string):
    global current_section
    current_section=string