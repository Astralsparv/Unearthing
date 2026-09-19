import shutil
import sys
import re

WIDTH,HEIGHT=shutil.get_terminal_size(fallback=(184,24))
buffer=[[(" ","") for _ in range(WIDTH)] for _ in range(HEIGHT)]
printx,printy=0,0

# regex magic
ANSI_RE=re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

def resize():
    global WIDTH, HEIGHT, buffer

    new_width,new_height=shutil.get_terminal_size(fallback=(184,24))

    if (new_width==WIDTH and new_height==HEIGHT):
        return

    WIDTH=new_width
    HEIGHT=new_height
    buffer=[[(" ","") for _ in range(WIDTH)] for _ in range(HEIGHT)]

def clear():
    resize()
    global buffer,printx,printy
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

def draw_at(x,y,string):
    for line in string.split("\n"):
        draw_line(x, y, line)
        y+=1
    
def draw_line(x,y,string):
    if (not (0<=y<HEIGHT)):
        return

    ansi=""

    px=x
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

        if (0<=px<WIDTH):
            buffer[y][px]=(char,ansi)

        px+=1
        pos+=1

def cprint(string):
    global printx, printy
    draw_at(printx,printy,string)
    printy+=string.count("\n") + 1

def cprintxy(string,x,y):
    global printx, printy
    printx=x
    printy=y
    draw_at(printx,printy,string)
    printy+=string.count("\n") + 1

def render(r=3,c=1): # render the buffer at cell,row
    # turn the 2d array (the buffer) into a multi-line string
    output=[]

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