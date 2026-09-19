from graphics import draw_at,cprint,clear,render,curs,curs_offset,draw_at_col
from tiles import tile_render,is_interactable,tiles,tile_name
import manager
from manager import mset, mget, set_map_programatically, text
from tiles import is_solid,passthrough_item_required,is_interactable,is_mineable
from items import give_loot_table, give_item, can_use, item_properties
from manager import get_key, current_item
from util import chance,wrap
import time

action_text=""

inventory_selection=-1
direction=None
action=None

def get_affected_area(properties,x,y,dx,dy):
    area=[]
    r_if=properties["range_infront"]
    if (dx==1 or dx==-1):
        if (r_if[0]):
            area.append([x,y-1])
        if (r_if[1]):
            area.append([x,y])
        if (r_if[2]):
            area.append([x,y+1])
    if (dy==1 or dy==-1):
        if (r_if[0]):
            area.append([x-1,y])
        if (r_if[1]):
            area.append([x,y])
        if (r_if[2]):
            area.append([x+1,y])
    return area

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
    for i in range(len(player["inventory"])): # needs a cap
        if (i==selected):
            txt+=get_item_print(player["inventory"][i]["item"],player["inventory"][i]["count"],True)+" "
        else:
            txt+=get_item_print(player["inventory"][i]["item"],player["inventory"][i]["count"])+" "
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
    curs(0,manager.current_map["height"]+2)

    cprint(text("ui.inventory"))
    draw_hotbar(manager.player["selected_inventory_slot"])

    curs(manager.current_map["width"]+4,6)
    cprint(wrap(action_text,80-manager.current_map["width"]-4))

    render()

direction_as_word={
    "w": "up",
    "a": "left",
    "s": "down",
    "d": "right"
}

def mine(x,y,dmg):
    global action_text
    # damage is currently irrelevant...
    tile=mget(x,y)
    mineable=is_mineable(tile)
    if (mineable):
        # always breaks, tile durability needed
        tile_display=text(f"tile.{tile_name(tile)}")
        action_text+="\n"+text("actions.pickaxe.hit_break",[tile_display])

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
        action_text+="\n"+text("actions.pickaxe.hit_nothing")

def attack(x,y,dmg):
    return
def update_player_actions():
    global direction, action, action_text
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
        manager.player["selected_inventory_slot"]-=1
        if (manager.player["selected_inventory_slot"]<0):
            manager.player["selected_inventory_slot"]=len(manager.player["inventory"])-1
    elif (key=="RIGHT"):
        manager.player["selected_inventory_slot"]+=1
        if (manager.player["selected_inventory_slot"]>=len(manager.player["inventory"])):
            manager.player["selected_inventory_slot"]=0

    if (direction!=None):
        if (action==None):
            action_text=text(f"actions.move.plan_{direction_as_word[direction]}")
        else:
            if (action=="q"):
                c=current_item()
                if (can_use(c)):
                    action_text=text(f"actions.{c["item"]}.plan_{direction_as_word[direction]}")
                else:
                    action=None
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
            c=current_item()
            if (can_use(c)):
                action_text=text(f"actions.{c["item"]}.plan")
            else:
                action=None
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
            dx,dy=0,0
            if (direction=="a"):
                x-=1
                dx=-1
            if (direction=="d"):
                x+=1
                dx=1
            if (direction=="w"):
                y-=1
                dy=-1
            if (direction=="s"):
                y+=1
                dy=1
            
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
            elif (action=="q"):
                c=current_item()
                if (direction):
                    action_text=text(f"actions.{c["item"]}.plan_{direction_as_word[direction]}")
                else:
                    action_text=text(f"actions.{c["item"]}.plan")

                properties=item_properties(c)
                # do animation!
                if (properties["animation"]=="tile_infront"):
                    draw_at_col(x,y,"X",fgcol=255)
                    render()
                    time.sleep(0.05)
                    draw_at_col(x,y,"*",fgcol=255)
                    render()
                    time.sleep(0.05)
                elif (properties["animation"]=="swipe_infront"):
                    if (dx==1 or dx==-1):
                        draw_at_col(x,y-1,",",fgcol=255)
                        render()
                        time.sleep(0.005)
                        if (dx==1):
                            draw_at_col(x,y,")",fgcol=255)
                        else:
                            draw_at_col(x,y,"(",fgcol=255)
                        render()
                        time.sleep(0.005)
                        draw_at_col(x,y+1,"'",fgcol=255)
                        render()
                        time.sleep(0.09)
                    if (dy==1 or dy==-1):
                        sym="'"
                        if (dy==-1):
                            sym='.'
                        draw_at_col(x-1,y,sym,fgcol=255)
                        render()
                        time.sleep(0.005)
                        draw_at_col(x,y,"-",fgcol=255)
                        render()
                        time.sleep(0.005)
                        draw_at_col(x+1,y,sym,fgcol=255)
                        render()
                        time.sleep(0.09)
                if ("damage_tiles" in properties):
                    affected=get_affected_area(properties,x,y,dx,dy)
                    for loc in affected:
                        mine(loc[0],loc[1],properties["damage_tiles"])
                if ("damage_enemies" in properties):
                    affected=get_affected_area(properties,x,y,dx,dy)
                    for loc in affected:
                        attack(loc[0],loc[1],properties["damage_enemies"])
        else:
            action_text=text("actions.nothing.do")
        action=None
        direction=None
    

def update():
    global action_text
    update_player_actions()