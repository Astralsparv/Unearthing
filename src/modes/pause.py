from graphics import clear,cprint,render,curs_offset
from manager import set_section,text
from manager import get_key
from font import load_font,render_str
import time

font=load_font("pico")

def resume():
    set_section("caving")

def save():
    set_section("save")

options=[
    {
        "label":"pause.resume",
        "func": resume
    },
    {
        "label":"pause.save",
        "func":save
    },
    {
        "label":"pause.exit",
        "func":exit
    }
]

current_option=0
scroll=0
txt_len=len(render_str(font,"paused    ").split("\n")[0])
last_scroll=time.monotonic()

def draw():
    global scroll,last_scroll

    clear()
    cprint(render_str(font,"paused    paused    paused"),offsetX=scroll)

    now=time.monotonic()
    dt=now-last_scroll
    last_scroll=now
    scroll-=10*dt
    if (scroll<=-txt_len):
        scroll+=txt_len
    
    for ind,opt in enumerate(options):
        curs_offset(0,1)
        str=""
        if (current_option==ind):
            str="> "
        str+=f"{text(opt["label"])}"
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
        resume()

    # when going oob, goes to other side
    if (current_option<0):
        current_option=len(options)-1
    elif (current_option>=len(options)):
        current_option=0
    
    if (key=="ENTER"):
        options[current_option]["func"]()