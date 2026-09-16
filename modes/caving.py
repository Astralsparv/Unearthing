from graphics import clear,draw_at
from tiles import tile_render,is_interactable,tiles,tile_name
import manager
from manager import mget, set_map_programatically, text
from random import randrange as randfloat

action_text=""
prior_action_text=""

printx,printy=0,0

def cprint(str):
    global printx, printy
    draw_at(printx,printy,str)
    printy+=1

def cprintxy(str,x,y):
    global printx, printy
    printx=x
    printy=y
    draw_at(printx,printy,str)
    printy+=1

def draw():
    global printx,printy,action_text
    c,r=1,5

    for y in range(manager.current_map["height"]):
        for x in range(manager.current_map["width"]):
            t=mget(x,y)
#            if (t==" "):
#                t=";"
            draw_at(x+c,y+r,tile_render(t))

    draw_at(c+manager.player["x"],r+manager.player["y"],"@")

    # draw a line between the two to seperate map&player data section
    
    # +2 means 2 extra
    for i in range(manager.current_map["height"]+2):
        # should be 4+i, but doing 3+i with the +2 above makes the line x2 than the map
        draw_at(manager.current_map["width"]+2,3+i,"|") # go to right of map +1 (full length) +1 (padding)

    # player data

    player=manager.player
    printx=manager.current_map["width"]+4
    printy=8
    cprint(player["name"])
    cprint(f"Health: {player['health']}/{player['max_health']}")
    cprintxy(text("ui.inventory"),printx,11)
    for k in player["inventory"]:
        label=f"item.{k}"
        cprint(f"{text(label)} x{player['inventory'][k]}")

    printy=4
    # draw a little display of the player so that they can see what they are on top of
    tile=tile_render(mget(player["x"],player["y"]))
    cprint(f"{tile}{tile}{tile}")
    cprint(f"{tile}@{tile}")
    cprint(f"{tile}{tile}{tile}")

    # print action text; describes what you just did
    printx=0
    printy=manager.current_map["height"]+5
    oy=manager.current_map["height"]
    textspl=prior_action_text.split("\n")
    # clear prior action text
    for i in range(len(textspl)):
        for j in range(len(textspl[i])):
            draw_at(j,i+oy+5," ")
    cprint(action_text)

    if (False): # debug
        printx+=5
        printy=2
        cprint(f"map w,h: {manager.current_map["width"]},{manager.current_map["height"]}")
        cprint(f"player x,y: {manager.player["x"]},{manager.player["y"]}")
        cprint(f"{manager.current_map["ladder_spots"]}")
#        cprint(f"{is_interactable(mget(player["x"],player["y"]))} {mget(player["x"],player["y"])}")
#        cprint(f"{tiles[mget(player["x"],player["y"])]}")

    # make sure random cell isn't selected and doesn't block UI
    draw_at(0,0,"")

import manager
from manager import mget,mset
from tiles import is_solid,passthrough_item_required,is_interactable,is_mineable
from inventory import give_loot_table, give_item

def update():
    global action_text,prior_action_text
    draw_at(0,0,"") #reset cursor loc

    prior_action_text=action_text
    action_text=""

    full=input("")
    for i in range(len(full)): # hide text input
        draw_at(i,1," ")
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
                    interaction,extra=is_interactable(tile)
                    if (interaction=="pickup"):
                        give_item(manager.player,extra,1)
                        item_name=text(f"item.{extra}")
                        # will need updating to figure out whether it is 'a item' or 'the item'
                        action_text+="\n"+text("actions.new_item.get_singular_a",[item_name])
                        mset(x,y,".")
                    elif (interaction=="go_to"):
                        set_map_programatically(extra)
            if (secondary=="q"): #attack or mine, default to mine for now; when hotbar added check that
                # assume mining
                tile=mget(x,y)
                mineable=is_mineable(tile)
                if (mineable):
                    # always breaks, tile durability needed
                    tile_display=text(f"tile.{tile_name(tile)}")
                    action_text+="\n"+text("actions.pickaxe.hit_tile_break",[tile_display])

                    mset(x,y,mineable["becomes"])
                    loot_given=give_loot_table(manager.player,mineable["loot_table"])

                    for item in loot_given:
                        count=loot_given[item]
                        item_name=text(f"item.{item}")
                        if (count==1):
                            # will need updating to figure out whether it is 'a item' or 'the item'
                            action_text+="\n"+text("actions.new_item.get_singular_a",[item_name])
                        else:
                            action_text+="\n"+text("actions.new_item.get_plural",[count,item_name])
                    
                    if ("ladder_spot" in tiles[tile]):
                        chance=(1/manager.current_map["ladder_spots"])*100
                        manager.current_map["ladder_spots"]-=1
                        if (manager.current_map["ladder_spots"]==0):
                            mset(x,y,"o") #ensure is always a ladder
                            if (manager.current_map["ladder_spawned"]==False):
                                action_text+="\n"+text("ladder_emerges.first_time_tile",[tile_display])
                            else:
                                action_text+="\n"+text("ladder_emerges.plural_time_tile",[tile_display])
                            manager.current_map["ladder_spawned"]=True
                        elif (randfloat(0,100)<=chance):
                            mset(x,y,"o")
                            if (manager.current_map["ladder_spawned"]==False):
                                action_text+="\n"+text("ladder_emerges.first_time_tile",[tile_display])
                            else:
                                action_text+="\n"+text("ladder_emerges.plural_time_tile",[tile_display])
                            manager.current_map["ladder_spawned"]=True
                else:
                    action_text=text("actions.pickaxe.hit_nothing")