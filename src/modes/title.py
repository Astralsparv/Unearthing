from graphics import clear,cprint,render
from manager import set_section,text
from manager import get_key
from font import load_font,render_str
import time

font=load_font("title")

options=[
    {
        "label":"title.new_game",
        "section":"caving"
    },
    {
        "label":"title.manual",
        "section":"manual"
    }
]

current_option=0
scroll=0
txt_len=len(render_str(font,"the unearthing  ").split("\n")[0])
last_scroll=time.monotonic()
def draw():
    global scroll,last_scroll

    clear()
    cprint(render_str(font,"the unearthing  the unearthing"),offsetX=scroll)

    now=time.monotonic()
    dt=now-last_scroll
    last_scroll=now
    scroll-=10*dt
    if (scroll<=-txt_len):
        scroll+=txt_len
    
    for ind,opt in enumerate(options):
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

    # when going oob, goes to other side
    if (current_option<0):
        current_option=len(options)-1
    elif (current_option>=len(options)):
        current_option=0
    
    if (key=="ENTER"):
        if ("section" in options[current_option]):
            set_section(options[current_option]["section"])