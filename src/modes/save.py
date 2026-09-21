from graphics import clear,cprint,render,curs_offset
from manager import set_section,text
from manager import get_key
import manager
from font import load_font,render_str
from save import saveData,loadData

import time

SAVE_SLOTS=5
font=load_font("pico")

def save():
    set_section("pause")

current_option=0
scroll=0
txt_len=len(render_str(font,"save game    ").split("\n")[0])
last_scroll=time.monotonic()

def draw():
    global scroll,last_scroll

    clear()
    cprint(render_str(font,"save game    save game    save game    "),offsetX=scroll)

    now=time.monotonic()
    dt=now-last_scroll
    last_scroll=now
    scroll-=10*dt
    if (scroll<=-txt_len):
        scroll+=txt_len

    for i in range(1,SAVE_SLOTS):
        str=f"{text("save.save_slot")} {i}"
        cprint(str)
    for i in range(1,SAVE_SLOTS):
        str=f"{text("save.load_slot")} {i}"
        cprint(str)
    
    render()
    
def update():
    global current_option
    key=get_key(timeout=0.01)
    if (key==None):
        return
    if (key=="RIGHT" or key=="DOWN"):
        current_option+=1
    if (key=="LEFT" or key=="UP"):
        current_option-=1
    if (key=="p" or key=="ESC"):
        set_section("caving")

    # when going oob, goes to other side
    if (current_option<0):
        current_option=(SAVE_SLOTS*2)-1
    elif (current_option>=(SAVE_SLOTS*2)):
        current_option=0
    
    if (key=="ENTER"):
        slot=current_option
        if (SAVE_SLOTS<current_option):
            slot-=SAVE_SLOTS
            save=loadData(slot)
            manager.player=save["player"]
            manager.current_map=save["map"]
        else:
            save={
                "player": manager.player,
                "map": manager.current_map
            }
            saveData(save,slot)