from graphics import draw_at,cprint,clear,render,curs,curs_offset,draw_at_col
from tiles import tile_render,is_interactable,tiles,tile_name
import manager
from manager import mset, mget, set_map_programatically, text
from tiles import is_solid,passthrough_item_required,is_interactable,is_mineable
from items import give_loot_table, give_item, can_use, item_properties
from manager import get_key, current_item
from util import chance,wrap

from modes.caving.helper import getActionText, rendering_game
import modes.caving.player as cplayer

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

def draw_map(x,y,w,h,dx=0,dy=0):
    x=int(x)
    y=int(y)
    # map
    for yy in range(h):
        for xx in range(w):
            t=mget(x+xx,y+yy)
            draw_at(dx+x+xx,dy+y+yy,tile_render(t))

def draw():
    map_w=30
    map_h=15

    cx,cy=rendering_game(True)

    draw_map(0,0,100,100)

    # draw player
    draw_at(manager.player["x"],manager.player["y"],"@")

    rendering_game(False)

    # bored around map
    
    for y in range(map_h):
        draw_at(map_w,y,"|")
    for x in range(map_w):
        draw_at(x,map_h,"-")
    draw_at(map_w,map_h,"'")

    # player data

    player=manager.player
    curs(map_w+2,0)
    cprint(player["name"])
    cprint(f"Health: {player['health']}/{player['max_health']}")

    # draw a little display of the player so that they can see what they are on top of
    tile=tile_render(mget(player["x"],player["y"]))
    cprint(f"{tile}{tile}{tile}")
    cprint(f"{tile}@{tile}")
    cprint(f"{tile}{tile}{tile}")

    # inventory

    # print below map text
    curs(1,map_h+1)
    cprint(text("ui.inventory"))
    draw_hotbar(manager.player["selected_inventory_slot"])

    curs(map_w+2,6)

    str=""
    direction=cplayer.direction
    action=cplayer.action
    if (direction):
        str+=direction
        if (action):
            str+=" > "+action
    elif (action):
        str+=action
    cprint(str)
    cprint(wrap(getActionText(),80-map_w-4))