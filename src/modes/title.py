from graphics import clear,cprint,render
from manager import set_section,text
from manager import get_key
from font import load_font,render_str

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

def draw():
    clear()
    cprint(render_str(font,"the unearthing"))
    
    for ind,opt in enumerate(options):
        str=""
        if (current_option==ind):
            str="> "
        str+=f"{text(opt["label"])}"
        cprint(str)
    render()
    
def update():
    global current_option
    key=get_key()
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