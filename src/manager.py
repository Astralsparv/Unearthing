from map import map_load, map_get, map_set, spawn_ores
from random import randint
from graphics import clear
from text import getLang,getText
from input import Keyboard
from tiles import can_spawn_ores

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
    "inventory": [
        {
            "item": "pickaxe",
            "count": 1
        },
        {
            "item": "sword",
            "count": 1
        }
    ],
    "selected_inventory_slot": 0
}

def current_item():
    global player
    return player["inventory"][player["selected_inventory_slot"]]

def set_map_programatically(map_type):
    clear() # avoid clear(), but is usually needed and easiest here when switching screens
    global current_map
    global player

    map=""
    if (map_type=="new_cave"):
        map=f"caves/{randint(0,5)}"
    current_map,player["x"],player["y"]=map_load(f"assets/maps/{map}")
    gen_map()

def set_map(map):
    clear() # avoid clear(), but is usually needed and easiest here when switching screens
    global current_map
    global player

    current_map,player["x"],player["y"]=map_load(f"assets/maps/{map}")

def gen_map():
    global current_map
    global player

    ore_spots=0
    for x in range(current_map["width"]):
        for y in range(current_map["height"]):
            if (can_spawn_ores(mget(x,y))):
                ore_spots+=1
    ores_needed=max(ore_spots/10,5)
    loops=0
    while loops<50 and ores_needed>0: # spawn_ores returns the amount of ores spawned
        # keep spawning until ores are spawned (OR safety of 50 loops, avoid inf loop)
        ores_needed-=spawn_ores(current_map,player["x"],player["y"])
        loops+=1

def set_lang(lang):
    global language
    language=getLang(lang)

def mget(x,y):
    return map_get(x,y,current_map)

def mset(x,y,v):
    map_set(x,y,v,current_map)

def set_section(string):
    global current_section
    clear() # avoid clear(), but is usually needed and easiest here when switching screens
    current_section=string

def text(fullid,opts=[]):
    global language
    return getText(language,fullid,opts)

keyboard=Keyboard()
keyboard.setup()

def get_key(timeout=None):
    return keyboard.get_key(timeout=timeout)