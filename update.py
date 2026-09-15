import manager
from manager import mget,mset
from tiles import solids,water,items

def update():
    key=input("")
    if (len(key)>1):
        key=key[len(key)-1]
    if (len(key)==1):
        x,y=manager.player["x"],manager.player["y"]
        if (key=="a"):
            x-=1
        if (key=="d"):
            x+=1
        if (key=="w"):
            y-=1
        if (key=="s"):
            y+=1
        tile=mget(x,y)
        can_move=True
        if (tile in solids):
            can_move=False
        if (tile in water):
            if (not "floatie" in manager.player["inventory"]):
                can_move=False
        if (can_move):
            manager.player["x"]=x
            manager.player["y"]=y
            if (key=="e"):
                if (tile in items):
                    manager.player["inventory"][items[tile]]=1
                    mset(x,y,".")