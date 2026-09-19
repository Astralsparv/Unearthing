from graphics import clear_fullscreen
from manager import set_map,set_map_programatically,gen_map,set_section,set_lang
import manager
from gameloop import draw, update
# sys
from time import sleep,perf_counter

clear_fullscreen()


#set_map("cave/0")
#set_map("cave/2")
#set_map("test")
set_lang("en-uk")
set_map_programatically("new_cave")

set_section("title")

import os
import ctypes
if os.name == "nt":
    kernel32 = ctypes.windll.kernel32

    stdout = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()

    if kernel32.GetConsoleMode(stdout, ctypes.byref(mode)):
        kernel32.SetConsoleMode(stdout, mode.value | 0x0004)
# sleep at 1/60 - 60fps
draw() # make so you dont need to make an action to see screen for first time
while True:
    start=perf_counter() # time at start of funcs
    update()
    draw()

    elapsed=perf_counter()-start # (time at end)-(start) = elapsed
    sleep(max(0,(1/30)-elapsed)) # dont spend more time if the frame took too long