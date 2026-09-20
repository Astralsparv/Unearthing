from graphics import set_camera,set_viewport
from animations import animate
import manager

action_text=""

def setActionText(string):
    global action_text
    action_text=string

def appendActionText(string):
    global action_text
    action_text+="\n"+string

def getActionText():
    return action_text

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

animations=[]
def add_anim_needed(name,x,y,dx=0,dy=0):
    animations.append({
        "name":name,
        "x":x,
        "y":y,
        "dx":dx,
        "dy":dy
    })

def do_needed_animations():
    while len(animations)>0:
        a=animations.pop(0)
        animate(a["name"],a["x"],a["y"],dx=a["dx"],dy=a["dy"])

def rendering_game(yes):
    if (yes):
        w=30
        h=15
        cx=manager.player["x"]-w/2
        cy=manager.player["y"]-h/2
        set_camera(x=cx,y=cy)
        set_viewport(x=0,y=0,w=w,h=h)
        return cx,cy
    else:
        set_camera()
        set_viewport()