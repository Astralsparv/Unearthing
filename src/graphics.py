import shutil
import sys
import re
from ansi import col
WIDTH,HEIGHT=80,24
buffer=[[(" ","") for _ in range(WIDTH)] for _ in range(HEIGHT)]
printx,printy=0,0

# regex magic
ANSI_RE=re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

viewport={
    "x": 0,
    "y": 0,
    "w": WIDTH,
    "h": HEIGHT
}

camera={
    "x":0,
    "y":0
}
def set_viewport(x=0,y=0,w=WIDTH,h=HEIGHT):
    global viewport
    viewport={
        "x":int(x),
        "y":int(y),
        "w":int(w),
        "h":int(h),
    }

def set_camera(x=None,y=None):
    global camera
    if (x==None and y==None):
        camera={"x":0,"y":0}
        return

    if (x!=None):
        camera["x"]=int(x)
    if (y!=None):
        camera["y"]=int(y)

def clear_fullscreen():
    w,h=shutil.get_terminal_size()

    txt=""
    for y in range(h):
        txt+=" "*w
    
    sys.stdout.write(txt)
    sys.stdout.flush() # no flash
def clear():
    global buffer,printx,printy,viewport
    viewport={
        "x": 0,
        "y": 0,
        "w": WIDTH,
        "h": HEIGHT
    }

    printx,printy=0,0
    buffer=[[(" ","") for _ in range(WIDTH)] for _ in range(HEIGHT)]

def curs(x=None,y=None):
    global printx,printy
    if (x!=None):
        printx=x
    if (y!=None):
        printy=y
    return printx,printy

def curs_offset(x=None,y=None):
    global printx,printy
    if (x!=None):
        printx+=x
    if (y!=None):
        printy+=y
    return printx,printy

def get_char(x,y):
    x-=camera["x"]
    y-=camera["y"]
    if (not (0<=x<viewport["w"])):
        return ("","")

    if (not (0<=y<viewport["h"])):
        return ("","")

    x+=viewport["x"]
    y+=viewport["y"]

    if (not (0<=x<WIDTH)):
        return ("","")
    if (not (0<=y<HEIGHT)):
        return ("","")
    return buffer[y][x]

def draw_at_prec(x,y,string,ansi):
    x=int(x)
    y=int(y)

    global buffer
    string=str(string)
    ansi=str(ansi)

    x-=camera["x"]
    y-=camera["y"]
    
    if (not (0<=x<viewport["w"])):
        return

    if (not (0<=y<viewport["h"])):
        return

    x+=viewport["x"]
    y+=viewport["y"]

    if (not (0<=x<WIDTH)):
        return

    if (not (0<=y<HEIGHT)):
        return
    
    buffer[y][x]=(string,ansi)

def draw_at(x,y,string,offsetX=0,offsetY=0):
    x=int(x)
    y=int(y)
    offsetX=int(offsetX)
    offsetY=int(offsetY)
    string=str(string)
    for line in string.split("\n"):
        draw_line(x, y, line,offsetX=offsetX,offsetY=offsetY)
        y+=1

def draw_at_col(x,y,string,offsetX=0,offsetY=0,bgcol=None,fgcol=None):
    x=int(x)
    y=int(y)
    offsetX=int(offsetX)
    offsetY=int(offsetY)
    string=col(str(string),bgcol=bgcol,fgcol=fgcol)
    draw_at(x,y,string,offsetX=offsetX,offsetY=offsetY)
    
def draw_line(x,y,string,offsetX=0,offsetY=0):
    x=int(x)
    y=int(y)
    offsetX=int(offsetX)
    offsetY=int(offsetY)

    y+=offsetY

    ansi=""

    px=x+offsetX
    pos=0

    while pos<len(string): #ansi handling
        match=ANSI_RE.match(string,pos)
        if (match):
            # ansi sequence
            seq=match.group(0)
            if (seq=="\033[0m"):
                ansi=""
            else:
                ansi+=seq
            
            pos=match.end()
            continue # straight to next iteration
        
        char=string[pos]

        draw_at_prec(px,y,char,ansi)

        px+=1
        pos+=1

def cprint(string,offsetX=0,offsetY=0):
    string=str(string)
    global printx, printy
    draw_at(printx,printy,string,offsetX=offsetX,offsetY=offsetY)
    printy+=string.count("\n")+1

def render(r=1,c=1): # render the buffer at cell,row
    # turn the 2d array (the buffer) into a multi-line string
    w,h=shutil.get_terminal_size()

    output=[] # ansi magic means you only need one output thing
    if (True and (WIDTH<w or HEIGHT<h)):
        left=c
        top=r
        right=c+WIDTH+1
        bottom=r+HEIGHT+1

        # top
        output.append(f"\033[{top};{left}H")
        output.append("."+"-"*(WIDTH)+".")

        # bottom
        output.append(f"\033[{bottom};{left}H")
        output.append("'"+"-"*(WIDTH)+"'")

        # sides
        for y in range(HEIGHT):
            output.append(f"\033[{top + y + 1};{left}H")
            output.append("|")

            output.append(f"\033[{top + y + 1};{right}H")
            output.append("|")
        if (h>HEIGHT):
            r+=1
        if (w>WIDTH):
            c+=1

    for y,row in enumerate(buffer):
        output.append(f"\033[{r+y};{c}H")

        cstyle=None

        for char,style in row:
            if cstyle!=style:
                output.append("\033[0m") # reset formatting
                output.append(style)
                cstyle=style
            output.append(char)

        output.append("\033[0m") # reset formatting

    sys.stdout.write("".join(output))
    sys.stdout.flush() # no flash