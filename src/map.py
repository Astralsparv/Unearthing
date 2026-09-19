#
# Maps are .txt files
# The width of the first line should be the longest width.
# They are loaded with map_load(filepath) and become an array
# where x,y of map == map[y][x]
#

from random import randint
from util import chance
from tiles import char_to_tile, tile_render, can_spawn_ores, tiles, get_ore_to_spawn

def randomDir():
    d=randint(0,3)
    if (d==0):
        return -1,0
    elif (d==1):
        return 1,0
    elif (d==2):
        return 0,-1
    elif (d==3):
        return 0,1

def map_get(x,y,map):
    if (len(map["data"])<=y):
        return 0
    elif (len(map["data"][y])<=x):
        return 0
    else:
        return map["data"][y][x]

def map_set(x,y,v,map):
    if (isinstance(v,str)):
        map["data"][y][x]=char_to_tile[v]
    else:
        map["data"][y][x]=v

def map_load(map_src):
    # convert map.txt -> 2d array
    # also get player char (where @ is)

    px=0
    py=0

    mapdat=[]
    ladder_spots=0
    with open(f"{map_src}.txt","r") as f:
        mapdat=f.read().split("\n") # full .txt into rows
    for i in range(len(mapdat)):
        mapdat[i]=list(mapdat[i]) # each row into row,column (y,x)
        for j in range(len(mapdat[i])):
            char=mapdat[i][j]
            if (char=="@"): # player
                px=j
                py=i
                mapdat[i][j]=char_to_tile["."]
            else:
                mapdat[i][j]=char_to_tile[mapdat[i][j]]
            if ("ladder_spawn" in tiles[mapdat[i][j]]):
                mapdat[i][j]=" "
                ladder_spots+=1
    
    map={
        "data":mapdat,
        "width":len(mapdat[0]),
        "height":len(mapdat),
        "ladder_spots":ladder_spots,
        "ladder_spawned": False
    }
    
    return map,px,py

# spawn ores in valid locations in the given map
# ix,iy == player x,y == cannot spawn

def spawn_ores(map,ix,iy):
    ores_spawned=0
    for y in range(map["height"]):
        for x in range(map["width"]):
            if (x!=ix and y!=iy):
                t=map_get(x,y,map)
                ore_chance=can_spawn_ores(t)
                if (chance(ore_chance)):
                    map_set(x,y,get_ore_to_spawn(),map)
                    ores_spawned+=1
                    if ("ladder_spot" in tiles[map_get(x,y,map)]):
                        map["ladder_spots"]+=1
    return ores_spawned