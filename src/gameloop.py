import modes.caving as caving, modes.title as title
import manager

def update():
    if (manager.current_section=="title"):
        title.update()
    elif (manager.current_section=="caving"):
        caving.update()

def draw():
    if (manager.current_section=="title"):
        title.draw()
    elif (manager.current_section=="caving"):
        caving.draw()