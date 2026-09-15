from update import update
from draw import draw
from manager import set_map
import manager

set_map("test.txt")

for i in range(100):
    print("")
draw()
while True:
    update()
    draw()