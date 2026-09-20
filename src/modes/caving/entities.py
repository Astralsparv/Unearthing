from graphics import draw_at,cprint,clear,render,curs,curs_offset,draw_at_col,set_viewport
from tiles import tile_render,is_interactable,tiles,tile_name
import manager
from manager import mset, mget, set_map_programatically, text
from tiles import is_solid,passthrough_item_required,is_interactable,is_mineable,can_spawn_enemies
from items import give_loot_table, give_item, can_use, item_properties, has_item
from manager import get_key, current_item
from util import chance,wrap,direction_as_word
from animations import animate
from random import randint

from modes.caving.helper import rendering_game

projectile={
    "arrow":{
        "sprites":{
            "left": "-",
            "right": "-",
            "up": "|",
            "down": "|"
        }
    }
}

entities={
    "archer":{
        "sprites":{
            "reloading": "]",
            "inactive": ")",
            "active": "}"
        },
        "health":5,
        "attack": "ranged",
        "projectile": "arrow",
        "ammo": 1,
        "reload_time": 4, # 4 turns
        "delay": 2, # 1 turn,
        "update_time":2
    },
    "bat":{
        "sprites":{
            "active": "\"",
        },
        "health": 2,
        "attack": "none", # no active effort to attack player
        "contact_damage": 1,
        "delay": 1,
        "pathfinding": {
            "inactive":{
                "type": "none"
            },
            "active":{
                "type": "pace",
                "steps": 2
            }
        },
        "update_time":2
    }
}

active_entities=[]

# ignore player always
def can_move_tile(x,y):
    tile=mget(x,y)
    if (is_solid(tile)):
        return False
    return True

def can_move(x,y,ignorePlayer=False):
    tile=mget(x,y)
    if (is_solid(tile)):
        return False,"solid"
    elif (ignorePlayer==False and manager.player["x"]==x and manager.player["y"]==y):
        return False,"player"
    return True,""

def pathfind(alg,ent):
    if (alg["type"]=="none"):
        return []
    path=[]
    if (alg["type"]=="pace"):
        x,y=ent["x"],ent["y"]
        
        for i in range(alg["steps"]):
            wx,wy=x,y
            wx+=ent["facingX"]
            wy+=ent["facingY"]
            if (can_move_tile(wx,wy,)):
                x,y=wx,wy
                path.append({"x":x,"y":y})
            elif (can_move_tile(wx,y) and x!=wx):
                x=wx
                path.append({"x":x,"y":y})
            elif (can_move_tile(x,wy) and y!=wy):
                y=wy
                path.append({"x":x,"y":y})
            else:
                ent["facingX"]*=-1
                ent["facingY"]*=-1
                i-=1 #give another step
    return path

def spawn_entity(x,y,type,facingX=1,facingY=0,state="active"):
    ent=entities[type]
    active_entities.append({
        "x":x,
        "y":y,
        "facingX": facingX,
        "facingY": facingY,
        "type":type,
        "health":ent["health"],
        "max_health":ent["health"],
        "state": state,
        "update_time": 0
    })

def attack_player(dmg):
    rendering_game(True)
    x,y=manager.player["x"],manager.player["y"]
    animate("damage_player",x,y)
    manager.player["health"]-=dmg
    rendering_game(False)

def damage_entities(x,y,dmg):
    global active_entities
    for ent in active_entities:
        if (ent["x"]==x and ent["y"]==y):
            ent["health"]-=dmg

def update_entities():
    global active_entities

    # lets checks be run for things to delete entity
    # probably will only be ent["health"]<=0 but still
    active_entities[:]=[
        ent for ent in active_entities
        if ent["health"]>0
    ]

    for ent in active_entities:
        dat=entities[ent["type"]]
        if (ent["update_time"]==dat["update_time"]):
            if (not "path" in ent or len(ent["path"])==0):
                ent["path"]=pathfind(dat["pathfinding"][ent["state"]],ent)
            if (len(ent["path"])>0):
                loc=ent["path"][0]
                can,why=can_move(loc["x"],loc["y"])
                if (can):
                    ent["x"]=loc["x"]
                    ent["y"]=loc["y"]
                    ent["path"].pop(0)
                else:
                    if (why=="player"):
                        if ("contact_damage" in dat):
                            attack_player(dat["contact_damage"])
                    else:
                        ent["path"]=pathfind(dat["pathfinding"][ent["state"]],ent)
            ent["update_time"]=0
        else:
            ent["update_time"]+=1

def draw_entities():
    global active_entities
    rendering_game(True)

    for ent in active_entities:
        dat=entities[ent["type"]]
        sp=dat["sprites"][ent["state"]]
        draw_at(ent["x"],ent["y"],sp)
    rendering_game(False)


entity_spawns=[
    {
        "type":"bat",
        "chance":50
    }
]

def spawn_entities():
    active_entities=[]
    for x in range(manager.current_map["width"]):
        for y in range(manager.current_map["height"]):
            v=can_spawn_enemies(mget(x,y))
            if (chance(v)):
                for _,entity in enumerate(entity_spawns):
                    if (chance(entity["chance"])):
                        facing=randint(1,4)
                        facingX=0
                        facingY=0
                        if (facing==0):
                            facingX=-1
                        if (facing==1):
                            facingX=1
                        if (facing==2):
                            facingY=-1
                        if (facing==3):
                            facingY=-1
                        spawn_entity(x,y,entity["type"],facingX=facingX,facingY=facingY)