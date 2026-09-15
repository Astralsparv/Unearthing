#
# Maps are .txt files
# The width of the first line should be the longest width.
# They are loaded with map_load(filepath) and become an array
# where x,y of map == map[y][x]
#

from ansi import pretty

def map_get(x,y,map):
    return map["data"][y][x]

def map_set(x,y,v,map):
    map["data"][y][x]=v

def map_load(map_src):
    # convert map.txt -> 2d array
    # also get player char (where @ is)

    px=0
    py=0

    mapdat=[]
    with open(map_src,"r") as f:
        mapdat=f.read().split("\n") # full .txt into rows
    for i in range(len(mapdat)):
        mapdat[i]=list(mapdat[i]) # each row into row,column (y,x)
        for j in range(len(mapdat[i])):
            char=mapdat[i][j]
            if (char=="@"): # player
                px=i
                py=j
                mapdat[i][j]="."
                break
    
    map={
        "data":mapdat,
        "width":len(mapdat[0]),
        "height":len(mapdat),
    }
    
    return map,px,py

def map_render(map):
    txt=""
    for y in range(map["height"]):
        for x in range(map["width"]):
            t=map_get(x,y,map)
            txt+=pretty(t)
        txt+="\n"
    return txt