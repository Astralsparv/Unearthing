from graphics import clear,draw_at
from tiles import tile_render,is_interactable,tiles
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
    clear()
    print("The Unearthing")
    

import manager
from manager import mget,mset
from tiles import is_solid,passthrough_item_required,is_interactable,is_mineable
from inventory import give_loot_table, give_item

def update():
    input("")