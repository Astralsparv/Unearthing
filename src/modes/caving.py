from graphics import draw_at,cprint,clear,render,curs,curs_offset
from tiles import tile_render,is_interactable,tiles,tile_name
import manager
from manager import mset, mget, set_map_programatically, text
from tiles import is_solid,passthrough_item_required,is_interactable,is_mineable
from inventory import give_loot_table, give_item
from manager import get_key
from util import chance

action_text=""

inventory_selection=-1
direction=None
action=None

def get_item_print(item,count,selected=False):
    label=text(f'item.{item}')
    if (selected):
        txt=f"<{label} x{count}>"
    else:
        txt=f"[{label} x{count}]"
    return txt

def draw_hotbar(selected):
    player=manager.player
    txt=""
    for n,k in enumerate(player["inventory"]):
        if (n==selected):
            txt+=get_item_print(k,player["inventory"][k],True)+" "
        else:
            txt+=get_item_print(k,player["inventory"][k])+" "
    cprint(txt)

def draw():
    global action_text
    global inventory_selection
    clear()

    map_w=manager.current_map["width"]
    map_h=manager.current_map["height"]

    # map
    for y in range(map_h):
        for x in range(map_w):
            t=mget(x,y)
            draw_at(x,y,tile_render(t))

    # player
    draw_at(manager.player["x"],manager.player["y"],"@")

    # seperator between map and player info
    
    for y in range(map_h):
        draw_at(map_w+2,y,"|")

    # player data

    player=manager.player
    curs(map_w+4,0)
    cprint(player["name"])
    cprint(f"Health: {player['health']}/{player['max_health']}")

    # draw a little display of the player so that they can see what they are on top of
    tile=tile_render(mget(player["x"],player["y"]))
    cprint(f"{tile}{tile}{tile}")
    cprint(f"{tile}@{tile}")
    cprint(f"{tile}{tile}{tile}")

    # inventory

    # print below map text
    curs(0,manager.current_map["height"]+5)

    cprint(text("ui.inventory"))
    draw_hotbar(inventory_selection)

    cprint(action_text)
    if (True): # debug
        curs(map_w+15,5)
        cprint(f"map w,h: {manager.current_map['width']},{manager.current_map['height']}")
        cprint(f"player x,y: {manager.player['x']},{manager.player['y']}")
        cprint(f"{manager.current_map['ladder_spots']}")
#        cprint(f"{is_interactable(mget(player["x"],player["y"]))} {mget(player["x"],player["y"])}")
#        cprint(f"{tiles[mget(player["x"],player["y"])]}")

    render()

direction_as_word={
    "w": "up",
    "a": "left",
    "s": "down",
    "d": "right"
}

def update_player_actions():
    global direction, action, action_text
    global inventory_selection
    key=get_key()
    if (key==None):
        action_text=text("actions.nothing.plan")
        return
    if (key in ("w","a","s","d")):
        if (direction==key):
            direction=None
        else:
            direction=key
            action=None
    elif (key in ("e","q")):
        if (action==key):
            action=None
        else:
            action=key
    elif (key=="LEFT"):
        inventory_selection-=1
        if (inventory_selection<0):
            inventory_selection=len(manager.player["inventory"])-1
    elif (key=="RIGHT"):
        inventory_selection+=1
        if (inventory_selection>=len(manager.player["inventory"])):
            inventory_selection=0

    if (direction!=None):
        if (action==None):
            action_text=text(f"actions.move.plan_{direction_as_word[direction]}")
        else:
            if (action=="q"):
                action_text=text(f"actions.pickaxe.plan_{direction_as_word[direction]}")
            elif (action=="e"):
                x,y=manager.player["x"],manager.player["y"]
                if (direction=="a"):
                    x-=1
                if (direction=="d"):
                    x+=1
                if (direction=="w"):
                    y-=1
                if (direction=="s"):
                    y+=1
                tile=mget(x,y)
                interaction,extra=is_interactable(tile)
                if (interaction):
                    if (interaction=="pickup"):
                        action_text=text(f"actions.pickup.plan_{direction_as_word[direction]}")
                    elif (interaction=="go_to"):
                        if (tiles[tile]["name"]=="ladder"):
                            action_text=text(f"actions.use_ladder.plan_{direction_as_word[direction]}")
                        elif (tiles[tile]["name"]=="shaft"):
                            action_text=text(f"actions.use_shaft.plan_{direction_as_word[direction]}")
                        else:
                            action_text=f"actions.???.plan_{direction_as_word[direction]} ;;;; action text not handled"
                    else:
                        action_text=f"actions.???.plan_{direction_as_word[direction]} ;;;; action text not handled"
                else:
                    action=None # not interactable
    elif (action!=None):
        if (action=="q"):
            action_text=text(f"actions.pickaxe.plan")
        elif (action=="e"):
            x,y=manager.player["x"],manager.player["y"]
            tile=mget(x,y)
            interaction,extra=is_interactable(tile)
            if (interaction):
                if (interaction=="pickup"):
                    action_text=text(f"actions.pickup.plan")
                elif (interaction=="go_to"):
                    if (tiles[tile]["name"]=="ladder"):
                        action_text=text(f"actions.ladder.plan")
                    elif (tiles[tile]["name"]=="shaft"):
                        action_text=text(f"actions.shaft.plan")
                    else:
                        action_text=f"actions.???.plan ;;;; action text not handled"
                else:
                    action_text=f"actions.???.plan ;;;; action text not handled"
            else:
                action=None # not interactable
    else:
        action_text=text("actions.nothing.plan")
    
    if (key=="ENTER"): # act!!!!!
        if ((direction is not None) or (action is not None)):
            x,y=manager.player["x"],manager.player["y"]
            if (direction=="a"):
                x-=1
            if (direction=="d"):
                x+=1
            if (direction=="w"):
                y-=1
            if (direction=="s"):
                y+=1
            
            tile=mget(x,y)
            can_move=True
            if (action!=None):
                can_move=False
            
            if (is_solid(tile)):
                can_move=False
            item_req_passthrough=passthrough_item_required(tile)
            if (item_req_passthrough!=None):
                if (not item_req_passthrough in manager.player["inventory"]):
                    can_move=False
            if (can_move):
                manager.player["x"]=x
                manager.player["y"]=y
                if (action==None):
                    tile=mget(x,y)
                    label=text(f"tile.{tiles[tile]['name']}")
                    action_text=text(f"actions.move.{direction_as_word[direction]}",[label])
            if (action=="e"):
                interaction,extra=is_interactable(tile)
                if (interaction=="pickup"):
                    give_item(manager.player,extra,1)
                    item_name=text(f"item.{extra}")
                    # will need updating to figure out whether it is 'a item' or 'the item' or 'item'
                    action_text+="\n"+text("actions.new_item.get_singular_a",[item_name])
                    mset(x,y,".")
                elif (interaction=="go_to"):
                    set_map_programatically(extra)
            elif (action=="q"): #attack or mine, default to mine for now; when hotbar added check that
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
                        perc=(1/manager.current_map["ladder_spots"])*100
                        manager.current_map["ladder_spots"]-=1
                        if (manager.current_map["ladder_spots"]==0):
                            mset(x,y,"o") #ensure is always a ladder
                            if (manager.current_map["ladder_spawned"]==False):
                                action_text+="\n"+text("ladder_emerges.first_time_tile",[tile_display])
                            else:
                                action_text+="\n"+text("ladder_emerges.plural_time_tile",[tile_display])
                            manager.current_map["ladder_spawned"]=True
                        elif (chance(perc)):
                            mset(x,y,"o")
                            if (manager.current_map["ladder_spawned"]==False):
                                action_text+="\n"+text("ladder_emerges.first_time_tile",[tile_display])
                            else:
                                action_text+="\n"+text("ladder_emerges.plural_time_tile",[tile_display])
                            manager.current_map["ladder_spawned"]=True
                else:
                    action_text=text("actions.pickaxe.hit_nothing")
        else:
            action_text=text("actions.nothing.do")
        action=None
        direction=None
    

def update():
    global action_text
    update_player_actions()