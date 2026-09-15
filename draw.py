from graphics import clear,draw_at
from ansi import pretty
from map import map_render
import manager
from manager import mget

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
    global printx,printy
    clear()
    print("\n\n")
    c,r=1,3
    print(map_render(manager.current_map))

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
    cprint(f"Health: {player["health"]}/{player["max_health"]}")
    cprintxy("Inventory",printx,11)
    for k in player["inventory"]:
        cprint(f"{k} x{player["inventory"][k]}")

    printy=4
    # draw a little display of the player so that they can see what they are on top of
    tile=pretty(mget(player["x"],player["y"]))
    cprint(f"{tile}{tile}{tile}")
    cprint(f"{tile}@{tile}")
    cprint(f"{tile}{tile}{tile}")

    # make sure current cell
    draw_at(0,0,"")