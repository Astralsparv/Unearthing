from graphics import clear
from manager import set_map,gen_map
import manager

#set_map("cave/0")
set_map("cave/2")
#set_map("test")
gen_map()

# avoid anything from previous runtimes flooding
clear()
for i in range(100):
    print("")



manager.draw() # make so you dont need to make an action to see screen for first time
while True:
    manager.update()
    manager.draw()