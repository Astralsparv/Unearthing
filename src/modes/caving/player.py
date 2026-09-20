from graphics import draw_at,cprint,clear,render,curs,curs_offset,draw_at_col
from tiles import tile_render,is_interactable,tiles,tile_name
import manager
from manager import mset, mget, set_map_programatically, text
from tiles import is_solid,passthrough_item_required,is_interactable,is_mineable
from items import give_loot_table, give_item, can_use, item_properties, has_item
from manager import get_key, current_item
from util import chance,wrap,direction_as_word
from animations import animate

from modes.caving.helper import setActionText,appendActionText, get_affected_area, add_anim_needed, rendering_game
from modes.caving.entities import damage_entities, spawn_entities

direction=None
action=None

def do_tile_animation(tile,x,y):
    if (tile>=0 and len(tiles)>tile):
        if ("animation" in tiles[tile]):
            animate(tiles[tile]["animation"],x,y)

def mine(x,y,dmg):
    # damage is currently irrelevant...
    tile=mget(x,y)
    mineable=is_mineable(tile)
    if (mineable):
        # always breaks, tile durability needed
        tile_display=text(f"tile.{tile_name(tile)}")
        appendActionText(text("actions.pickaxe.hit_break",[tile_display]))

        mset(x,y,mineable["becomes"])
        loot_given=give_loot_table(manager.player,mineable["loot_table"])

        for item in loot_given:
            count=loot_given[item]
            item_name=text(f"item.{item}")
            if (count==1):
                # will need updating to figure out whether it is 'a item' or 'the item'
                appendActionText(text("actions.new_item.get_singular_a",[item_name]))
            else:
                appendActionText(text("actions.new_item.get_plural",[count,item_name]))
        
        if ("ladder_spot" in tiles[tile]):
            perc=(1/manager.current_map["ladder_spots"])*100
            manager.current_map["ladder_spots"]-=1
            if (manager.current_map["ladder_spots"]==0):
                mset(x,y,"o") #ensure is always a ladder
                if (manager.current_map["ladder_spawned"]==False):
                    appendActionText(text("ladder_emerges.first_time_tile",[tile_display]))
                else:
                    appendActionText(text("ladder_emerges.plural_time_tile",[tile_display]))
                manager.current_map["ladder_spawned"]=True
            elif (chance(perc)):
                mset(x,y,"o")
                if (manager.current_map["ladder_spawned"]==False):
                    appendActionText(text("ladder_emerges.first_time_tile",[tile_display]))
                else:
                    appendActionText(text("ladder_emerges.plural_time_tile",[tile_display]))
                manager.current_map["ladder_spawned"]=True
    else:
        appendActionText(text("actions.pickaxe.hit_nothing"))

def attack(x,y,dmg):
    damage_entities(x,y,dmg)

def update_player_actions():
    global direction, action, action_text
    key=get_key()
    if (key==None):
        setActionText(text("actions.nothing.plan"))
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
            setActionText(text(f"actions.move.plan_{direction_as_word[direction]}"))
        else:
            if (action=="q"):
                c=current_item()
                if (can_use(c)):
                    setActionText(text(f"actions.{c["item"]}.plan_{direction_as_word[direction]}"))
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
                        setActionText(text(f"actions.pickup.plan_{direction_as_word[direction]}"))
                    elif (interaction=="go_to"):
                        if (tiles[tile]["name"]=="ladder"):
                            setActionText(text(f"actions.use_ladder.plan_{direction_as_word[direction]}"))
                        elif (tiles[tile]["name"]=="shaft"):
                            setActionText(text(f"actions.use_shaft.plan_{direction_as_word[direction]}"))
                        else:
                            setActionText(f"actions.???.plan_{direction_as_word[direction]} ;;;; action text not handled")
                    else:
                        setActionText(f"actions.???.plan_{direction_as_word[direction]} ;;;; action text not handled")
                else:
                    action=None # not interactable
    elif (action!=None):
        if (action=="q"):
            c=current_item()
            if (can_use(c)):
                setActionText(text(f"actions.{c["item"]}.plan"))
            else:
                action=None
        elif (action=="e"):
            x,y=manager.player["x"],manager.player["y"]
            tile=mget(x,y)
            interaction,extra=is_interactable(tile)
            if (interaction):
                if (interaction=="pickup"):
                    setActionText(text(f"actions.pickup.plan"))
                elif (interaction=="go_to"):
                    if (tiles[tile]["name"]=="ladder"):
                        setActionText(text(f"actions.ladder.plan"))
                    elif (tiles[tile]["name"]=="shaft"):
                        setActionText(text(f"actions.shaft.plan"))
                    else:
                        setActionText(f"actions.???.plan ;;;; action text not handled")
                else:
                    setActionText(f"actions.???.plan ;;;; action text not handled")
            else:
                action=None # not interactable
    else:
        setActionText(text("actions.nothing.plan"))
    
    if (key=="ENTER"): # act!!!!!
        rendering_game(True)
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
                if (not has_item(manager.player,item_req_passthrough)):
                    can_move=False
            if (can_move):
                manager.player["x"]=x
                manager.player["y"]=y
                if (action==None):
                    tile=mget(x,y)
                    label=text(f"tile.{tiles[tile]['name']}")
                    setActionText(text(f"actions.move.{direction_as_word[direction]}",[label]))
            if (action=="e"):
                do_tile_animation(tile,x,y)
                interaction,extra=is_interactable(tile)
                if (interaction=="pickup"):
                    give_item(manager.player,extra,1)
                    item_name=text(f"item.{extra}")
                    # will need updating to figure out whether it is 'a item' or 'the item' or 'item'
                    appendActionText(text("actions.new_item.get_singular_a",[item_name]))
                    mset(x,y,".")
                elif (interaction=="go_to"):
                    animate("circle_in",x,y)
                    set_map_programatically(extra)
                    spawn_entities()
                    add_anim_needed("circle_out",manager.player["x"],manager.player["y"])
            elif (action=="q"):
                c=current_item()
                if (direction):
                    setActionText(text(f"actions.{c["item"]}.plan_{direction_as_word[direction]}"))
                else:
                    setActionText(text(f"actions.{c["item"]}.plan"))

                properties=item_properties(c)

                if ("animation" in properties):
                    animate(properties["animation"],x,y,dx,dy)
                if ("damage_tiles" in properties):
                    affected=get_affected_area(properties,x,y,dx,dy)
                    for loc in affected:
                        mine(loc[0],loc[1],properties["damage_tiles"])
                if ("damage_enemies" in properties):
                    affected=get_affected_area(properties,x,y,dx,dy)
                    for loc in affected:
                        attack(loc[0],loc[1],properties["damage_enemies"])
        else:
            setActionText(text("actions.nothing.do"))
        action=None
        direction=None
        rendering_game(False)
        return True