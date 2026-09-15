from update import update
from draw import draw
from manager import set_map,gen_map
import manager

#set_map("cave/0")
set_map("cave/2")
#set_map("test")
gen_map()

for i in range(100):
    print("")
draw()

while True:
    update()
    draw()