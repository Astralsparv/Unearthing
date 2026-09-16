from graphics import clear
from manager import set_map,set_map_programatically,gen_map,set_section
import manager
from gameloop import draw, update

#set_map("cave/0")
#set_map("cave/2")
#set_map("test")
set_map_programatically("new_cave")

# avoid anything from previous runtimes flooding
clear()
for i in range(100):
    print("")

set_section("title")

draw() # make so you dont need to make an action to see screen for first time
while True:
    update()
    draw()