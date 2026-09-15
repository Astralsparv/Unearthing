import manager
from manager import mget,mset
from tiles import is_solid,passthrough_item_required,is_interactable,is_mineable
from inventory import give_loot_table, give_item

def update():
    full=input("")
    if (len(full)>0):
        primary=full[0] # primary action, interact on current tile or move
        secondary=""
        if (len(full)>1):
            secondary=full[1] or "" # secondary action is acted in direction of primary, primary no longer moves or picks up
        if (len(primary)==1):
            x,y=manager.player["x"],manager.player["y"]
            if (primary=="a"):
                x-=1
            if (primary=="d"):
                x+=1
            if (primary=="w"):
                y-=1
            if (primary=="s"):
                y+=1
            tile=mget(x,y)
            can_move=True
            if (secondary!=""):
                can_move=False
                primary=""
            
            if (is_solid(tile)):
                can_move=False
            item_req_passthrough=passthrough_item_required(tile)
            if (item_req_passthrough!=None):
                if (not item_req_passthrough in manager.player["inventory"]):
                    can_move=False
            if (can_move):
                manager.player["x"]=x
                manager.player["y"]=y
                if (primary=="e"):
                    interaction,new_item=is_interactable(tile)
                    if (interaction=="pickup"):
                        give_item(manager.player,new_item,1)
                        mset(x,y,".")
            if (secondary=="q"): #attack or mine, default to mine for now; when hotbar added check that
                # assume mining
                tile=mget(x,y)
                mineable=is_mineable(tile)
                if (mineable):
                    mset(x,y,mineable["becomes"])
                    give_loot_table(manager.player,mineable["loot_table"])