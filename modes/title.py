from graphics import clear,draw_at
from manager import set_section

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

title_text=""
with open("graphics/title.txt","r") as f:
    title_text=f.read()

options=[
    {
        "label":"Start Game",
        "section":"caving"
    },
    {
        "label":"Manual",
        "section":"manual"
    }
]

current_option=0

def draw():
    clear()
    print("\n\n")
    print(title_text)
    print("")

    for ind,opt in enumerate(options):
        str=""
        if (current_option==ind):
            str="> "
        str+=f"{opt["label"]}"
        print(str)
    
def update():
    global current_option
    key=input("")
    if (key=="d" or key=="s"):
        current_option+=1
    if (key=="a" or key=="w"):
        current_option-=1

    # when going oob, goes to other side
    if (current_option<0):
        current_option=len(options)-1
    elif (current_option>=len(options)):
        current_option=0
    
    if (key=="e"):
        if ("section" in options[current_option]):
            set_section(options[current_option]["section"])